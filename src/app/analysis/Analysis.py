from app.libs import *
from app.constants import DATA_DIR
from app.config import settings


LOG = logging.getLogger("app.analysis")

class ReplayAnalyzer:
    def __init__(self, replaypath: str, rep_basedir: str):
        self.replaypath = replaypath
        self.rep_basedir = rep_basedir
        self.rep_name = os.path.basename(replaypath)
        self.output_path = f"{rep_basedir}\\SC2RepAnalysis\\{self.rep_name}"
        self.replay = None
        self.duration = 0
        self.event_categories = {}

        # 加载配置数据
        self.Slist = self._load_toml(DATA_DIR / "unit.toml")["Slist"]
        self.Clist = self._load_toml(DATA_DIR / "change.toml")["Clist"]
        self.CClist = self._load_toml(DATA_DIR / "change.toml")["CClist"]
        self.CCClist = self._load_toml(DATA_DIR / "change.toml")["CCClist"]
        self.Ilist = self._load_toml(DATA_DIR / "build.toml")["Ilist"]
        self.upgrade_times = self._load_toml(DATA_DIR / "upgrade.toml")["Ulist"]

        self.unit_born_events = [] # 单位出生事件：未按时间和player分组
        self.full_unit_events = [] # 完整单位出生事件：未按时间和player分组
        self.unit_init_events = [] # 单位出生事件：按时间和player分组
        self.unit_change_events = [] # 单位变化事件：未按时间和player分组
        self.player_stats_events = [] # 玩家数据事件：未按时间和player分组

        # 存储分析结果
        self.Fullinf=[] # 完整单位信息
        self.UBE_List={}

        self.ube_players = {}  # 单位建造事件
        self.uie_players = {}  # 建筑建造事件
        self.uce_players = {}  # 单位变化事件
        self.ue_players = {}  # 科技升级事件
        self.ua_players = {}  # 当前存活单位
        self.pse_players = {}  # 人口/农民数据
        self.data_for_excel = {}  # 用于导出的数据
        self.summary_row = []   # 汇总行（用于 DataFrame）
        LOG.debug("初始化完成")

    @staticmethod
    def _load_toml(path):
        with open(path, "rb") as f:
            return tomllib.load(f)

    def analyze(self):
        """主分析入口"""
        try:
            self._load_replay()
            self._validate_replay()
            self._make_output_dir()
            self._categorize_events()

            # 执行各项分析
            self._collect_unit_born_events()
            self._collect_full_unit_events()
            self._format_data()
            self._calculate_unit_liveness()
            self._collect_upgrade_events()
            self._collect_building_events()
            self._collect_unit_type_changes()
            self._collect_player_stats()

            # 格式化与输出
            self._format_data_for_output()
            # self._write_text_report()
            # self._write_excel_reports()

            return 0
        except Exception as e:
            LOG.error("Analysis failed for %s: %s", self.rep_name, str(e))
            return -1

    def _load_replay(self):
        self.replay = load_replay(self.replaypath, load_level=4)
        self.duration = round(self.replay.frames / 16)
        LOG.debug("加载replay文件--ok")

    def _validate_replay(self):
        if self.duration < 8:
            raise ValueError(f"Game too short ({self.duration}s), skipped.")
        LOG.debug("校验replay文件有效性--ok")

    def _make_output_dir(self):
        os.makedirs(self.output_path, exist_ok=True)
        LOG.debug("创建输出目录--ok")

    def _categorize_events(self):
        event_names = {event.name for event in self.replay.events}
        self.event_categories = {name: [] for name in event_names}
        for event in self.replay.events:
            self.event_categories[event.name].append(event)
        LOG.debug("事件分类完成--ok")
    
    def _collect_unit_born_events(self):
        #--------------------------3.统计单位Born列表，并改为Build时间----------------------------#
        # 统计各位玩家的建造列表C
        self.ube_players={name:{} for name in self.replay.players} 
        #---------------------------------统计人口数量----------------------------------#
        #一共需要考虑两个项目：正在卵里的和死亡的，主要思路：变卵无条件加入，如果已经产好的项目进栈时，如果栈中已经有相同的单位，就不影响人口，死亡减去相应人口
        unit_born_events = self.event_categories["UnitBornEvent"]

        current_second=-1
        for i in unit_born_events:
            if i.unit.owner and i.unit.name!='InvisibleTargetDummy'and i.unit.name!='ParasiticBombRelayDummy' and i.unit.name!='ParasiticBombDummy'and i.unit.name!='BroodlingEscort' and i.unit.name!='Broodling' and i.unit.name!='Larva':
                while current_second!=i.second:
                #初始状态&到下一秒的情况：在UP中新建一个set
                #考虑特殊的情况：跳秒（该秒没有发生建造事件）
                    current_second+=1
                    for j in self.ube_players:
                        self.ube_players[j][current_second]=[]

                #处理本秒内的情况
                if i.unit.name in self.Slist and current_second!=0:
                    try:
                        self.ube_players[i.unit.owner][i.second-round(self.Slist[i.unit.name][1]*1.4)].append(self.Slist[i.unit.name][0])
                    except:
                        #开局加速生产探姬：临时解决办法-假设是全程加速生产
                        try: 
                            self.ube_players[i.unit.owner][i.second-round(self.Slist[i.unit.name][1]*1.4/1.5)].append(self.Slist[i.unit.name][0])
                        except: #如果还有特别的情况：例如特殊游戏模式更改了生产速度，就全部设置为其born的时刻
                            self.ube_players[i.unit.owner][i.second].append(self.Slist[i.unit.name][0])
                #else:
                #    ube_players[i.unit.owner][i.second].append(i.unit.name)
        LOG.debug("统计单位Bron列表--ok")
    
    def _collect_full_unit_events(self):
        full_unit_events=[
            self.event_categories.get("UnitBornEvent", []),
            self.event_categories.get("UnitDiedEvent", []),
            self.event_categories.get("UnitInitEvent", []),
            self.event_categories.get("UnitTypeChangeEvent", []),
        ]

        Ast={name:{} for name in self.replay.players}

        for I_event in full_unit_events:
            I_UBE={name:{} for name in self.replay.players}
            current_second=-1
            for j in I_event:
                if j.unit and j.unit.owner and (j.unit.name in self.Ilist or j.unit.name in self.Slist):
                    if j.second!=current_second:
                        while current_second!=j.second:
                            current_second+=1
                            for k in I_UBE:
                                I_UBE[k][current_second]=[]
                    if j.name =='UnitInitEvent' and j.unit.race=='Protoss' and j.unit.name in self.Slist and j.unit.name in self.Ilist:
                        if j.second+16>=len(self.Fullinf[0][j.unit.owner]):
                            while len(self.Fullinf[0][j.unit.owner])-16<=j.second:
                                n=len(self.Fullinf[0][j.unit.owner])
                                self.Fullinf[0][j.unit.owner][n]=[]
                        if j.unit.name=='Archon':
                            if j.unit.finished_at:
                                self.Fullinf[0][j.unit.owner][j.second].append("白球(正在融合)")
                                self.Fullinf[1][j.unit.owner][j.second+12].append("白球(正在融合)")
                                self.Fullinf[0][j.unit.owner][j.second+12].append(self.Slist[j.unit.name][0])
                                #对于正常融合完成的白球，在init时刻存活单位减少两个隐刀或电兵
                                if j.unit.finished_at in Ast[j.unit.owner]:
                                    self.Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.finished_at][0])
                                    del Ast[j.unit.owner][j.unit.finished_at][0]
                                    self.Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.finished_at][0])
                                    del Ast[j.unit.owner][j.unit.finished_at][0]
                                    if not Ast[j.unit.owner][j.unit.finished_at]:
                                        del Ast[j.unit.owner][j.unit.finished_at]
                            else:
                                #对于未正常融合完成的白球，在init时刻同理
                                if j.unit.died_at in Ast[j.unit.owner]:
                                    self.Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.died_at][0])
                                    del Ast[j.unit.owner][j.unit.died_at][0]
                                    self.Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.died_at][0])
                                    del Ast[j.unit.owner][j.unit.died_at][0]
                                    if not Ast[j.unit.owner][j.unit.died_at]:
                                        del Ast[j.unit.owner][j.unit.died_at]
                                self.Fullinf[0][j.unit.owner][j.second].append("白球(正在融合)")
                        else:
                            if j.unit.finished_at:
                                self.Fullinf[0][j.unit.owner][int(j.unit.finished_at/16)].append(self.Slist[j.unit.name][0])
                    elif j.name =='UnitInitEvent' and j.unit.race=='Zerg' and j.unit.name!='CreepTumorBurrowed' and j.unit.name!='CreepTumor' and j.unit.name!= 'CreepTumorQueen' and  j.unit.finished_at:
                        self.Fullinf[1][j.unit.owner][j.second].append(self.Slist['Drone'][0])
                    #if j.name == 'UnitTypeChangeEvent':
                    #    self.Fullinf[1][j.unit.owner][j.second].append(j.unit.name)
                    
                    elif j.name=='UnitTypeChangeEvent':
                        if j.second>=len(self.Fullinf[0][j.unit.owner]):
                            while len(self.Fullinf[0][j.unit.owner])-1<=j.second:
                                n=len(self.Fullinf[0][j.unit.owner])
                                self.Fullinf[0][j.unit.owner][n]=[]
                        #出生事件一定会发生，如果死亡事件没有发生，临时解决方案：跳过
                        if len(self.Fullinf)!=1:
                            if j.second>=len(self.Fullinf[1][j.unit.owner]):
                                while len(self.Fullinf[1][j.unit.owner])-1<=j.second:
                                    n=len(self.Fullinf[1][j.unit.owner])
                                    self.Fullinf[1][j.unit.owner][n]=[]

                        if j.unit_type_name in self.CClist:
                            for jj in j.unit.type_history: #统计何时是眼虫最近一次变异
                                if jj<j.frame:
                                    od=jj
                                else:
                                    op=jj
                                    break

                            if j.unit_type_name in ['OverseerSiegeModeCocoon','OverlordCocoon']: #变异为眼虫茧的情况
                                for ob in  j.unit.type_history:
                                    if j.unit.type_history[ob].str_id=="OverlordTransport": #过去是载货王虫
                                        self.Fullinf[0][j.unit.owner][j.second].append("眼虫茧")
                                        self.Fullinf[1][j.unit.owner][j.second].append("载货王虫")
                                        break
                                else: #否则就是房子变眼虫茧
                                    self.Fullinf[0][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][0])
                                    self.Fullinf[1][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][1])

                            elif j.unit_type_name== 'Overseer': #变为眼虫的情况
                                #print("眼虫变身！")
                                if j.unit.type_history[od].str_id!="OverseerSiegeMode": #过去不是视野眼虫，即过去是眼虫卵
                                    #print("过去不是视野眼虫！")
                                    self.Fullinf[0][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][0])
                                    self.Fullinf[1][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][1])
                                #else:
                                    #print("原来之前是视野眼虫，无视发生")
                                    
                            elif j.unit_type_name =="Overlord": #如果是取消变眼虫
                                self.Fullinf[0][j.unit.owner][j.second].append("房子")
                                self.Fullinf[1][j.unit.owner][j.second].append("眼虫茧")
                            elif j.unit_type_name =="OverlordTransport": #如果是取消变眼虫
                                if j.unit.type_history[od].str_id in ['OverseerSiegeModeCocoon','OverlordCocoon']:
                                    self.Fullinf[0][j.unit.owner][j.second].append("载货王虫")
                                    self.Fullinf[1][j.unit.owner][j.second].append("眼虫茧")
                                else:
                                    self.Fullinf[0][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][0])
                                    self.Fullinf[1][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][1])
                            else:
                                try:
                                    if j.unit.type_history[od].str_id[-8:]!="Burrowed":
                                        #print("变异单位：{}".format(self.CClist[j.unit_type_name][0]))
                                        self.Fullinf[0][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][0])
                                        self.Fullinf[1][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][1])
                                except:
                                    if op==jj:
                                        self.Fullinf[0][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][0])
                                        self.Fullinf[1][j.unit.owner][j.second].append(self.CClist[j.unit_type_name][1])
                    else:
                        if j.name!='UnitInitEvent' and (j.unit.name in self.Slist or j.unit.name not in self.Ilist):
                            if j.name=='UnitDiedEvent':
                                if j.killer:
                                    if j.unit.name=="Archon":
                                        if j.unit.finished_at:
                                            I_UBE[j.unit.owner][j.second].append(self.Slist[j.unit.name][0])
                                        else:
                                            I_UBE[j.unit.owner][j.second].append("白球(正在融合)")
                                    else:
                                        if j.unit.name in self.CClist:
                                            I_UBE[j.unit.owner][j.second].append(self.CClist[j.unit.name][0])
                                        elif j.unit.name in self.CCClist:
                                            I_UBE[j.unit.owner][j.second].append(self.CCClist[j.unit.name][0])
                                        else:
                                            if j.unit.finished_at or j.unit.finished_at==0:
                                                I_UBE[j.unit.owner][j.second].append(self.Slist[j.unit.name][0])
                                else:
                                    if j.unit.name=="DarkTemplar" or j.unit.name=='HighTemplar':
                                        if j.frame not in Ast[j.unit.owner]:
                                            Ast[j.unit.owner][j.frame]=[]
                                        Ast[j.unit.owner][j.frame].append(self.Slist[j.unit.name][0]) 
                            if j.name=='UnitBornEvent':
                                I_UBE[j.unit.owner][j.second].append(self.Slist[j.unit.name][0])
            self.Fullinf.append(I_UBE)
        LOG.debug("统计完整单位Bron列表--ok")
    
    def _format_data(self):
        for player in self.replay.players:
            self.UBE_List[player]={}
            for Buildevents in self.Fullinf: #对各类单位事件进行遍历
                for i in Buildevents[player]: #对各类单位事件按参赛者遍历每秒建造列表，i是字典的键
                    if i not in self.UBE_List[player]: #如果
                        self.UBE_List[player][i]=[]
                    self.UBE_List[player][i].append(Buildevents[player][i])
        LOG.debug("格式化数据--ok")
    
    def _calculate_unit_liveness(self):
        #------------------------------6.统计生存单位--------------------------------------#
        Unitalive={name:{} for name in self.replay.players}
        self.ua_players={name:{} for name in self.replay.players}
        for i in self.UBE_List: #遍历每个选手，i是选手名
            for j in self.UBE_List[i]: #遍历每秒，j是秒,除了第0秒之外，令当前秒等于上一秒
                if j!=0:
                    Unitalive[i][j]=Unitalive[i][j-1]
                else: 
                    Unitalive[i][j]={}
                for n in range(len(self.UBE_List[i][j])): #遍历每秒钟的出生项和死亡项,n=0为出生项，n=1为死亡项
                    for nn in self.UBE_List[i][j][n]:
                        if n==0:
                            if nn not in Unitalive[i][j]:
                                Unitalive[i][j][nn]=0
                            #print(Unitalive[i][j][nn])
                            Unitalive[i][j][nn]+=1
                        if n==1:
                            try: #如果因为某些原因在存活数量为0时还会死亡单位，就将该单位存活数量设定为0
                                Unitalive[i][j][nn]-=1
                            except:
                                Unitalive[i][j][nn]=0
                            if Unitalive[i][j][nn]==0:
                                del Unitalive[i][j][nn] 
                
                self.ua_players[i][j]=list(Unitalive[i][j].items())
        LOG.debug("统计生存单位--ok")

    def _collect_upgrade_events(self):
        """
        7.统计UpgradeCompleteEvent事件，记录科技升级
        """
        Upgrade_events=self.event_categories['UpgradeCompleteEvent']
        self.ue_players={name:{} for name in self.replay.players}
        current_second=-1

        for event in Upgrade_events:
            if event.upgrade_type_name in ['SprayZerg', 'SprayTerran', 'SprayProtoss']:
                continue
            if event.second!=current_second: 
                while current_second!=event.second:
                    current_second+=1
                    for j in self.ue_players:
                        self.ue_players[j][current_second]=[]
            if event.upgrade_type_name in self.upgrade_times and current_second!=0 and event.player:
                try:
                    self.ue_players[event.player][event.second-round(self.upgrade_times[event.upgrade_type_name][1]*1.4)].append(self.upgrade_times[event.upgrade_type_name][0])
                except:
                    self.ue_players[event.player][event.second].append(self.upgrade_times[event.upgrade_type_name][0]+"（升级完毕）")
            #else:
            #    ue_players[event.player][event.second].append(event.upgrade_type_name)
        LOG.debug("统计科技升级事件--ok")

    def _collect_building_events(self):
        if 'UnitInitEvent' in self.event_categories:
            self.unit_init_events = self.event_categories['UnitInitEvent']
            self.uie_players={name:{} for name in self.replay.players}
            current_second=-1
            for i in self.unit_init_events:
                if i.unit.owner:
                    if i.second!=current_second: 
                        while current_second!=i.second:
                            current_second+=1
                            for j in self.uie_players:
                                self.uie_players[j][current_second]=[]
                    if i.unit_type_name in self.Ilist and current_second!=0:
                        if i.unit_type_name in self.Slist:
                            if i.second>=len(self.ube_players[i.unit.owner]):
                                while len(self.ube_players[i.unit.owner])-1<=i.second:
                                    n=len(self.ube_players[i.unit.owner])
                                    self.ube_players[i.unit.owner][n]=[]
                            self.ube_players[i.unit.owner][i.second].append(self.Ilist[i.unit_type_name])
                        else:
                            if (not i.unit.finished_at) and (i.unit.killed_by==i.unit.owner) and i.unit_type_name!='CreepTumorBurrowed' and i.unit_type_name!='CreepTumor':
                                self.uie_players[i.unit.owner][i.second].append(self.Ilist[i.unit_type_name]+"（建造后取消）")
                            else: 
                                self.uie_players[i.unit.owner][i.second].append(self.Ilist[i.unit_type_name])
                    #else:
                    #    uie_players[i.unit.owner][i.second].append(i.unit.name)
        LOG.debug("统计建造事件--ok")

    def _collect_unit_type_changes(self):
        #--------------------------9.统计单位变异列表(目前全部合并到了单位建造和升级科技)----------------------------#
        if 'UnitTypeChangeEvent' in self.event_categories:
            self.unit_change_events = self.event_categories['UnitTypeChangeEvent']
            self.uce_players={name:{} for name in self.replay.players}
            current_second=-1

            for i in self.unit_change_events:
                if i.unit.owner and i.unit.name!='CreepTumorBurrowed'and i.unit.name!='CreepTumor'  and i.unit.name!='Larva':
                    if i.second!=current_second: 
                        while current_second!=i.second:
                            current_second+=1
                            for j in self.uce_players:
                                self.uce_players[j][current_second]=[]
                    if i.unit_type_name in self.Clist and current_second!=0:
                        #如果是虫族升本，就归类到科技升级上去
                        if i.unit_type_name=='Lair':
                            #处理科技升级时长列表长度不够的情况
                            if i.second-80>=len(self.ue_players[i.unit.owner]):
                                while len(self.ue_players[i.unit.owner])-1<=i.second-80:
                                    n=len(self.ue_players[i.unit.owner])
                                    self.ue_players[i.unit.owner][n]=[]
                            self.ue_players[i.unit.owner][i.second-80].append(self.Clist[i.unit_type_name])

                        elif i.unit_type_name in ['Hive','GreaterSpire']:
                            if i.second-99>=len(self.ue_players[i.unit.owner]):
                                while len(self.ue_players[i.unit.owner])-1<=i.second-99:
                                    n=len(self.ue_players[i.unit.owner])
                                    self.ue_players[i.unit.owner][n]=[]
                            self.ue_players[i.unit.owner][i.second-99].append(self.Clist[i.unit_type_name])
                            
                        elif i.unit_type_name =='OrbitalCommand':
                            for f in i.unit.type_history:
                                if i.unit.type_history[f].name=='OrbitalCommand' and f<i.frame:
                                    if i.second>=len(self.uie_players[i.unit.owner]):
                                        while len(self.uie_players[i.unit.owner])-1<=i.second:
                                            n=len(self.uie_players[i.unit.owner])
                                            self.uie_players[i.unit.owner][n]=[]
                                    #如果这个星轨过去就已经是星轨了！
                                    self.uie_players[i.unit.owner][i.second].append("星轨落地")
                                    break
                            else:
                                if i.second-35>=len(self.uie_players[i.unit.owner]):
                                    while len(self.uie_players[i.unit.owner])-1<=i.second-35:
                                        n=len(self.uie_players[i.unit.owner])
                                        self.uie_players[i.unit.owner][n]=[]
                                self.uie_players[i.unit.owner][i.second-35].append(self.Clist[i.unit_type_name])

                        elif i.unit_type_name=='PlanetaryFortress':
                            if i.second-50>=len(self.uie_players[i.unit.owner]):
                                while len(self.uie_players[i.unit.owner])-1<=i.second-50:
                                    n=len(self.uie_players[i.unit.owner])
                                    self.uie_players[i.unit.owner][n]=[]
                            self.uie_players[i.unit.owner][i.second-50].append(self.Clist[i.unit_type_name])
                        elif i.unit_type_name in self.Ilist: #对于剩余的单位变异，只剩下挂件类
                            if i.unit_type_name=='Reactor' or i.unit_type_name=='TechLab':
                                if i.second>=len(self.uie_players[i.unit.owner]):
                                    while len(self.uie_players[i.unit.owner])-1<=i.second:
                                        n=len(self.uie_players[i.unit.owner])
                                        self.uie_players[i.unit.owner][n]=[]
                                for f in i.unit.type_history:
                                    if f<i.frame:
                                        ff=i.unit.type_history[f].name
                                    else: #当遍历到此刻时，返回上一刻的内容
                                        if ff=='BarracksReactor':
                                            self.uie_players[i.unit.owner][i.second].append("双倍挂件脱离(兵营)")
                                        if ff=='BarracksTechLab':
                                            self.uie_players[i.unit.owner][i.second].append("科技挂件脱离(兵营)")
                                        if ff=='FactoryReactor':
                                            self.uie_players[i.unit.owner][i.second].append("双倍挂件脱离(重工厂)")
                                        if ff=='FactoryTechLab':
                                            self.uie_players[i.unit.owner][i.second].append("科技挂件脱离(重工厂)")
                                        if ff=='StarportReactor':
                                            self.uie_players[i.unit.owner][i.second].append("双倍挂件脱离(星港)")
                                        if ff=='StarportTechLab':
                                            self.uie_players[i.unit.owner][i.second].append("科技挂件脱离(星港)")
                                        break
                            else:
                                if i.second>=len(self.uie_players[i.unit.owner]):
                                    while len(self.uie_players[i.unit.owner])-1<=i.second:
                                        n=len(self.uie_players[i.unit.owner])
                                        self.uie_players[i.unit.owner][n]=[]
                                self.uie_players[i.unit.owner][i.second].append(self.Clist[i.unit_type_name])
                        else:
                            if i.second>=len(self.ube_players[i.unit.owner]):
                                while len(self.ube_players[i.unit.owner])-1<=i.second:
                                    n=len(self.ube_players[i.unit.owner])
                                    self.ube_players[i.unit.owner][n]=[]
                            self.ube_players[i.unit.owner][i.second].append(self.Clist[i.unit_type_name])
                    #else: #顺便列入其他变异项（埋地、由卵变单位等情况）
                        #uce_players[i.unit.owner][i.second].append(i.unit_type_name)
        LOG.debug("统计单位变异事件--ok")

    def _collect_player_stats(self):
        self.player_stats_events=self.event_categories['PlayerStatsEvent']
        self.pse_players={name:{} for name in self.replay.players}
        current_second=-1
        for i in self.player_stats_events:
            if i.second!=current_second: 
                while current_second!=i.second:
                    current_second+=1
                    for j in self.pse_players:
                        self.pse_players[j][current_second]=[]
            if current_second!=0:
                self.pse_players[i.player][i.second].append("{}/{}/{}".format(int(i.food_used),int(i.food_made),int(i.workers_active_count)))
        
        LOG.debug("统计人口信息--ok")
    def _format_data_for_output(self):
#-------------------------------11.格式化输出------------------------------------------#
        file = open('{}/{}.txt'.format(self.output_path,self.rep_name), 'w',encoding="utf-8")
        DataForPd={}
        PdS=[]
        for i in self.replay.players:
            file.write("选手{}的建造列表：".format(i)) 
            j=0
            DataForPd[i]=[]
            try:
                if i not in self.replay.winner:
                    whetherwin="负"
                else:
                    whetherwin="胜"
            except:
                whetherwin="无胜者"
            
            try:
                if i==self.replay.players[0]:
                    racebattle='{}v{}'.format(self.replay.players[0].play_race[0],self.replay.players[1].play_race[0])
                else:
                    racebattle='{}v{}'.format(self.replay.players[1].play_race[0],self.replay.players[0].play_race[0])
            except:
                racebattle='{}v{}'.format(self.replay.players[0].play_race[0],"None")
            PdS.append([re.match('\w{0,}',str(i)[11:]).group(),self.replay.map_name,i.play_race,racebattle,"{}:{}".format(round(self.duration/1.4)//60,round(self.duration/1.4)%60),whetherwin,"","","","{}".format(self.replaypath)])
            while j<self.duration:
                #---------------构造DataFrame格式的数据-----------------------------#
                s=[i,"{}:{}".format(round(j/1.4)//60,round(j/1.4)%60)]
                
                #----------------非常混沌的部分-数据整理：遍历各个项目，对重复的计数，对处于同一秒的整合-----------#
                if j<len(self.pse_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(self.pse_players[i]) and (self.pse_players[i][j] or self.pse_players[i][j+1]):
                        if self.pse_players[i][j]:
                            cc.append("{}".format(self.pse_players[i][j][0]))
                        else:
                            cc.append("{}".format(self.pse_players[i][j+1][0]))
                    else:
                        if self.pse_players[i][j]:
                            cc.append("{}".format(self.pse_players[i][j][0]))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")

                if j<len(self.ua_players[i]):
                    number=""
                    number1=""
                    for n in self.ua_players[i][j]:
                        if ('工蜂' in n) or('SCV' in n )or ('探姬' in n):
                            number=n[1]
                    cc=[]
                    if j+1<len(self.ua_players[i]):
                        for n in self.ua_players[i][j+1]:
                            if ('工蜂' in n) or('SCV' in n )or ('探姬' in n):
                                number1=n[1]

                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(self.ua_players[i]):
                        cc.append("{}".format(number1))
                    else:
                        cc.append("{}".format(number))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")    

                if j<len(self.ube_players[i]):
                    cc=[]
                    dd=[]
                    if round((j/1.4))==round(((j+1)/1.4)) and j+1<len(self.ube_players[i]):
                        dd.append(self.ube_players[i][j]+self.ube_players[i][j+1])
                        for c in Counter(self.ube_players[i][j]+self.ube_players[i][j+1]):
                            cc.append("{}*{}".format(c,Counter(self.ube_players[i][j]+self.ube_players[i][j+1])[c]))
                    else:
                        dd.append(self.ube_players[i][j])
                        for c in Counter(self.ube_players[i][j]):
                            cc.append("{}*{}".format(c,Counter(self.ube_players[i][j])[c]))
                    if cc:
                        s.append(','.join(cc))
                        for ddd in dd:
                            PdS[-1][8]+=','.join(ddd)+','
                    else:
                        s.append('')
                else:
                    s.append("")


                """if j<len(uce_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(uce_players[i]):
                        for c in Counter(uce_players[i][j]+uce_players[i][j+1]):
                            cc.append("{}*{}".format(c,Counter(uce_players[i][j]+uce_players[i][j+1])[c]))
                    else:
                        for c in Counter(uce_players[i][j]):
                            cc.append("{}*{}".format(c,Counter(uce_players[i][j])[c]))
                    s.append(cc)
                else:
                    s.append([])"""


                #在此处去除了菌毯对于流程分析的影响
                if 'UnitInitEvent' in self.event_categories:
                    if j<len(self.uie_players[i]):
                        cc=[]
                        dd=[]
                        if round(j/1.4)==round((j+1)/1.4) and j+1<len(self.uie_players[i]): 
                            for ccc in self.uie_players[i][j]+self.uie_players[i][j+1]:                     
                                if ('菌毯' not in ccc) and ("建造后取消" not in ccc) and ("防空管子" not in ccc)  and ("补给站" not in ccc) and ("水晶" not in ccc) and ("起飞" not in ccc) and ("脱离" not in ccc) and ("电池" not in ccc) and ("气矿" not in ccc):
                                    dd.append(ccc)  
                            for c in Counter(self.uie_players[i][j]+self.uie_players[i][j+1]):                        
                                cc.append("{}*{}".format(c,Counter(self.uie_players[i][j]+self.uie_players[i][j+1])[c]))
                        else:
                            for ccc in self.uie_players[i][j]:
                                if ('菌毯' not in ccc) and ("建造后取消" not in ccc) and ("防空管子" not in ccc)  and ("补给站" not in ccc) and ("水晶" not in ccc) and ("起飞" not in ccc) and ("脱离" not in ccc) and ("电池" not in ccc) and ("气矿" not in ccc):
                                    dd.append(ccc)
                            for c in Counter(self.uie_players[i][j]):
                                cc.append("{}*{}".format(c,Counter(self.uie_players[i][j])[c]))
                        if cc:
                            s.append(','.join(cc))
                            if dd:
                                PdS[-1][7]+=','.join(dd)+','
                        else:
                            s.append('')
                    else:
                        s.append("")
                else:
                    s.append("")

                    
                if j<len(self.ue_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(self.ue_players[i]):
                        for c in self.ue_players[i][j]+self.ue_players[i][j+1]:
                            cc.append(c)
                    else:
                        for c in self.ue_players[i][j]:
                            cc.append(c)
                    if cc:
                        s.append(','.join(cc))
                        PdS[-1][6]+=','.join(cc)+','
                    else:
                        s.append('')
                else:
                    s.append("")

                
                if j<len(self.ua_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(self.ua_players[i]):
                        cc.append("{}".format(self.ua_players[i][j+1]))
                    else:
                        cc.append("{}".format(self.ua_players[i][j]))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")

                #-----------------------处理该秒没有发生event的情况-----------------------------#
                tep="\n[{}]".format(s[1])
                if settings.fulltime=="yes":
                    DataForPd[i].append(s[1:])
                else:
                    if s[4] or s[5] or s[6]:           
                        if s[3]:
                            tep+="|农民{}|，".format(s[3])
                        if s[4]:
                            tep+="{}，".format(s[4])
                        if s[5]:
                            tep+="{}，".format(s[5])
                        if s[6]:
                            tep+="{}".format(s[6])
                        file.write(tep)
                        DataForPd[i].append(s[1:])
                #-------------------------------------------------#
                if round(j/1.4)==round((j+1)/1.4):
                    j+=1
                j+=1 
            file.write("\n-------------------------------------------------------------------------------\n")
        file.close()
        for i in DataForPd:
            Inf_to_excel = pd.DataFrame(DataForPd[i],columns=['时间','人口','农民','单位建造','建造建筑','科技升级','当前存活单位'])
            Inf_to_excel.to_excel("{}/{}的建造列表({}).xlsx".format(self.output_path,i,self.rep_name[:-10]),index=False)
        
        LOG.debug("格式化输出excel和txt--ok")

