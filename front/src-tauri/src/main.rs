use std::process::Stdio;
use std::sync::Arc;

use tauri::{AppHandle, Manager};
use tauri::Emitter; // ← 必须：emit 来自这个 trait
use tokio::{
  io::{AsyncBufReadExt, BufReader},
  process::{Child, Command},
  sync::Mutex,
};

use std::path::PathBuf;
fn find_project_root() -> PathBuf {
    let mut dir = std::env::current_dir().unwrap();
    loop {
        if dir.join(".project-root").exists() {
            return dir;
        }
        if !dir.pop() {
            break;
        }
    }
    std::env::current_dir().unwrap()
}

#[derive(Default)]
struct PyProc(Arc<Mutex<Option<Child>>>);

// 把子进程 stdout/stderr 的每一行转成事件发给前端
async fn read_and_emit<R: tokio::io::AsyncRead + Unpin + Send + 'static>(
  reader: R,
  app: AppHandle,
  event: &'static str,
) {
  let mut lines = BufReader::new(reader).lines();
  while let Ok(Some(line)) = lines.next_line().await {
    let _ = app.emit(event, line.clone());
  }
}

#[tauri::command]
async fn start_python(app: AppHandle, log_level: Option<String>) -> Result<(), String> {
  // 先发一条测试事件，确认前端监听正常
  let _ = app.emit("py:stdout", "tauri command received: start_python");

  // 根据你的环境选择 python/py/绝对路径
  let lvl = log_level.unwrap_or_else(|| "INFO".into());

  let root_dir = find_project_root();
  let src_dir = root_dir.join("src");

  let mut child = Command::new("python")
      .args(["-m", "app", "--log-level", &lvl,"alone"])
      .current_dir(&src_dir) // ✅ 设置工作目录
      .stdout(Stdio::piped())
      .stderr(Stdio::piped())
      .spawn()
      .map_err(|e| format!("spawn python failed: {e}"))?;


  let stdout = child.stdout.take().unwrap();
  let stderr = child.stderr.take().unwrap();

  let app_clone = app.clone();
  tauri::async_runtime::spawn(read_and_emit(stdout, app_clone, "py:stdout"));
  let app_clone = app.clone();
  tauri::async_runtime::spawn(read_and_emit(stderr, app_clone, "py:stderr"));

  // 保存子进程句柄
  let state = app.state::<PyProc>();
  *state.0.lock().await = Some(child);
  Ok(())
}

#[tauri::command]
async fn stop_python(app: AppHandle) -> Result<(), String> {
  let state = app.state::<PyProc>();
  if let Some(mut child) = state.0.lock().await.take() {
    let _ = child.kill().await;
    let _ = app.emit("py:stdout", "python process killed");
  }
  Ok(())
}

fn main() {
  tauri::Builder::default()
    .manage(PyProc::default()) // ← 构造并注册全局状态，否则会有“never constructed”
    .invoke_handler(tauri::generate_handler![start_python, stop_python]) // ← 注册命令
    .run(tauri::generate_context!())
    .expect("error while running tauri app");
}
