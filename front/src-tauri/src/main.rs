use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::io::Write;
use std::process::{Command, Stdio};
use tauri::path::BaseDirectory;
use tauri::{command, AppHandle, Manager};

// ---------- 数据结构 ----------
#[derive(Serialize, Deserialize)]
struct AnalyzeOptions {
    analyze_type: String,
    output_dir: String,
    basic: bool,
    bo: bool,
    actions: bool,
    units: bool,
    mapheat: bool,
    exportXlsx: bool,
    tz: String,
    lang: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalyzeResult {
    #[serde(rename = "map_name")]
    pub map_name: String,
    #[serde(rename = "ladder?", default)]
    pub ladder: bool,
    pub duration: u32,
    #[serde(rename = "playersInfo")]
    pub players_info: HashMap<String, PlayerInfo>,
    pub winner: String,
    pub region: String,
    #[serde(rename = "endTime")]
    end_time: Option<String>,
    #[serde(rename = "raceBattle")]
    pub race_battle: String,
    pub output: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct PlayerInfo {
    pub race: String,
    pub result: bool,
    pub buildOrder: Vec<BoStep>,
    pub outputPath: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BoStep {
    pub t: String,
    pub action: String,
}

// ---------- Tauri 命令 ----------
#[command]
async fn analyze_replay(
    app: AppHandle,
    path: String,
    options: AnalyzeOptions,
) -> Result<AnalyzeResult, String> {
    #[cfg(target_os = "windows")]
    let rel = "bin/main.exe";
    #[cfg(not(target_os = "windows"))]
    let rel = "bin/main";

    let py_bin = app
        .path()
        .resolve(rel, BaseDirectory::Resource)
        .map_err(|e| format!("resolve py bin error: {e}"))?;

    // 启动子进程
    let mut child = Command::new(py_bin)
        .arg("json")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .map_err(|e| format!("spawn error: {e}"))?;

    // 写入请求 JSON
    let input = serde_json::json!({
      "path": path,
      "options": options
    })
    .to_string();

    {
        let stdin = child.stdin.as_mut().ok_or("failed to open child stdin")?;
        stdin
            .write_all(input.as_bytes())
            .map_err(|e| format!("stdin write error: {e}"))?;
    }
    drop(child.stdin.take());

    // 等待子进程结束
    let output = child
        .wait_with_output()
        .map_err(|e| format!("wait_with_output error: {e}"))?;

    let stdout_text = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr_text = String::from_utf8_lossy(&output.stderr).to_string();

    println!("python stdout = {}", stdout_text);
    println!("python stderr = {}", stderr_text);

    if !output.status.success() {
        return Err(format!(
            "python exit code: {:?}\nstderr:\n{}",
            output.status, stderr_text
        ));
    }

    if stdout_text.trim().is_empty() {
        return Err(format!("python stdout is empty.\nstderr:\n{}", stderr_text));
    }

    let parsed: AnalyzeResult = serde_json::from_str(&stdout_text).map_err(|e| {
        format!(
            "JSON parse error: {e}\nstdout:\n{}\nstderr:\n{}",
            stdout_text, stderr_text
        )
    })?;

    Ok(parsed)
}

fn main() {
    println!("Hello, world!");
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .invoke_handler(tauri::generate_handler![analyze_replay])
        .run(tauri::generate_context!())
        .expect("error while running tauri app");
}
