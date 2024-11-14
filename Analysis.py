from head import *

def Analysis(replaypath,r,bar):
    try:
        def file_path(x):
            res=x
            name=os.path.basename(res)
            return sc2reader.load_replay(res,load_level=4),name
        
        replay,name=file_path(replaypath)
        Duration=round((replay.frames)/16)
        path="{}/SC2RepAnalysis/{}".format(r,name)
        if not os.path.exists(path):
            os.makedirs(path)
        if Duration<8:
            raise Exception("游戏时长为{}秒,时间过短，不进行分析".format(Duration))

        #---------------------------1.按类对Events进行分类------------------------------------#
        def get_event(replay):
            event_names = set([event.name for event in replay.events])
            events_of_type = {name: [] for name in event_names}
            for event in replay.events:
                events_of_type[event.name].append(event)
            return events_of_type
        a=get_event(replay)

        bar()

        #--------------------------3.统计单位Bron列表，并改为Build时间----------------------------#
            #---------------------------------统计人口数量----------------------------------#
            #一共需要考虑两个项目：正在卵里的和死亡的，主要思路：变卵无条件加入，如果已经产好的项目进栈时，如果栈中已经有相同的单位，就不影响人口，死亡减去相应人口

        unit_born_events = a["UnitBornEvent"]
        ube_players={name:{} for name in replay.players}
        #uBe_players={name:{} for name in replay.players}
        une_players={name:{} for name in replay.players}
        ntep_players={name:12 for name in replay.players}

        res=-1
        for i in unit_born_events:
            if i.unit.owner and i.unit.name!='InvisibleTargetDummy'and i.unit.name!='ParasiticBombRelayDummy' and i.unit.name!='ParasiticBombDummy'and i.unit.name!='BroodlingEscort' and i.unit.name!='Broodling' and i.unit.name!='Larva':
                #print(i.unit.name,i.second)
                if i.second!=res: 
                    while res!=i.second:
                    #初始状态&到下一秒的情况：在UP中新建一个set
                    #考虑特殊的情况：跳秒（该秒没有发生建造事件）
                        res+=1
                        for j in ube_players:
                            ube_players[j][res]=[]
                            #uBe_players[j][res]=[]
                    #print("当前时间为{}".format(i.second))
                    #print("s={},res={}".format(i.second,res))
                #处理本秒内的情况
                if i.unit.name in Slist and res!=0:
                    try:
                        ube_players[i.unit.owner][i.second-round(Slist[i.unit.name][1]*1.4)].append(Slist[i.unit.name][0])
                    except:
                        #开局加速生产探姬：临时解决办法-假设是全程加速生产
                        try: 
                            ube_players[i.unit.owner][i.second-round(Slist[i.unit.name][1]*1.4/1.5)].append(Slist[i.unit.name][0])
                        except: #如果还有特别的情况：特殊游戏模式更改了生产速度，就全部设置为其born的时刻
                            ube_players[i.unit.owner][i.second].append(Slist[i.unit.name][0])
                    #uBe_players[i.unit.owner][i.second].append(Slist[i.unit.name][0])
                #else:
                #    ube_players[i.unit.owner][i.second].append(i.unit.name)
                #    uBe_players[i.unit.owner][i.second].append(i.unit.name)
                    ntep_players[i.unit.owner]+=i.unit.supply

        bar()


        #------------------------------------4.批量统计：单位出生与死亡---------------------------#
        RelatedEvent=[a['UnitBornEvent']]
        if 'UnitDiedEvent' in a:
            RelatedEvent.append(a['UnitDiedEvent'])
        if 'UnitInitEvent' in a:
            RelatedEvent.append(a['UnitInitEvent'])
        if 'UnitTypeChangeEvent' in a:
            RelatedEvent.append(a['UnitTypeChangeEvent'])
        Fullinf=[]
        Ast={name:{} for name in replay.players}
        for i in RelatedEvent:
            I_UBE={name:{} for name in replay.players}
            I_event=i
            res=-1
            for j in I_event:
                if j.unit and j.unit.owner and (j.unit.name in Ilist or j.unit.name in Slist):
                    if j.second!=res:
                        while res!=j.second:
                            res+=1
                            for k in I_UBE:
                                I_UBE[k][res]=[]
                    if j.name =='UnitInitEvent' and j.unit.race=='Protoss' and j.unit.name in Slist and j.unit.name in Ilist:
                        if j.second+16>=len(Fullinf[0][j.unit.owner]):
                            while len(Fullinf[0][j.unit.owner])-16<=j.second:
                                n=len(Fullinf[0][j.unit.owner])
                                Fullinf[0][j.unit.owner][n]=[]
                        if j.unit.name=='Archon':
                            #print(Ast[j.unit.owner])
                            if j.unit.finished_at:
                                Fullinf[0][j.unit.owner][j.second].append("白球(正在融合)")
                                Fullinf[1][j.unit.owner][j.second+12].append("白球(正在融合)")
                                Fullinf[0][j.unit.owner][j.second+12].append(Slist[j.unit.name][0])
                                #对于正常融合完成的白球，在init时刻存活单位减少两个隐刀或电兵
                                if j.unit.finished_at in Ast[j.unit.owner]:
                                    #print("融合完成，消耗{}+{}".format(Ast[j.unit.owner][j.unit.finished_at][0],Ast[j.unit.owner][j.unit.finished_at][1]))
                                    Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.finished_at][0])
                                    del Ast[j.unit.owner][j.unit.finished_at][0]
                                    Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.finished_at][0])
                                    del Ast[j.unit.owner][j.unit.finished_at][0]
                                    if not Ast[j.unit.owner][j.unit.finished_at]:
                                        del Ast[j.unit.owner][j.unit.finished_at]
                            else:
                                #对于未正常融合完成的白球，在init时刻同理
                                if j.unit.died_at in Ast[j.unit.owner]:
                                    Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.died_at][0])
                                    del Ast[j.unit.owner][j.unit.died_at][0]
                                    Fullinf[1][j.unit.owner][j.second].append(Ast[j.unit.owner][j.unit.died_at][0])
                                    del Ast[j.unit.owner][j.unit.died_at][0]
                                    if not Ast[j.unit.owner][j.unit.died_at]:
                                        del Ast[j.unit.owner][j.unit.died_at]
                                Fullinf[0][j.unit.owner][j.second].append("白球(正在融合)")
                        else:
                            if j.unit.finished_at:
                                Fullinf[0][j.unit.owner][int(j.unit.finished_at/16)].append(Slist[j.unit.name][0])
                    elif j.name =='UnitInitEvent' and j.unit.race=='Zerg' and j.unit.name!='CreepTumorBurrowed' and j.unit.name!='CreepTumor' and j.unit.name!= 'CreepTumorQueen' and  j.unit.finished_at:
                        #print("时间{},变建筑{}".format(j.second,j.unit.name))
                        Fullinf[1][j.unit.owner][j.second].append(Slist['Drone'][0])
                    #if j.name == 'UnitTypeChangeEvent':
                    #    Fullinf[1][j.unit.owner][j.second].append(j.unit.name)
                    
                    elif j.name=='UnitTypeChangeEvent':
                        if j.second>=len(Fullinf[0][j.unit.owner]):
                            while len(Fullinf[0][j.unit.owner])-1<=j.second:
                                n=len(Fullinf[0][j.unit.owner])
                                Fullinf[0][j.unit.owner][n]=[]
                        #出生事件一定会发生，如果死亡事件没有发生，临时解决方案：跳过
                        if len(Fullinf)!=1:
                            if j.second>=len(Fullinf[1][j.unit.owner]):
                                while len(Fullinf[1][j.unit.owner])-1<=j.second:
                                    n=len(Fullinf[1][j.unit.owner])
                                    Fullinf[1][j.unit.owner][n]=[]

                        if j.unit_type_name in CClist:
                            for jj in j.unit.type_history: #统计何时是眼虫最近一次变异
                                if jj<j.frame:
                                    od=jj
                                else:
                                    op=jj
                                    break

                            if j.unit_type_name in ['OverseerSiegeModeCocoon','OverlordCocoon']: #变异为眼虫茧的情况
                                for ob in  j.unit.type_history:
                                    if j.unit.type_history[ob].str_id=="OverlordTransport": #过去是载货王虫
                                        Fullinf[0][j.unit.owner][j.second].append("眼虫茧")
                                        Fullinf[1][j.unit.owner][j.second].append("载货王虫")
                                        break
                                else: #否则就是房子变眼虫茧
                                    Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                    Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])

                            elif j.unit_type_name== 'Overseer': #变为眼虫的情况
                                #print("眼虫变身！")
                                if j.unit.type_history[od].str_id!="OverseerSiegeMode": #过去不是视野眼虫，即过去是眼虫卵
                                    #print("过去不是视野眼虫！")
                                    Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                    Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])
                                #else:
                                    #print("原来之前是视野眼虫，无视发生")
                                    
                            elif j.unit_type_name =="Overlord": #如果是取消变眼虫
                                Fullinf[0][j.unit.owner][j.second].append("房子")
                                Fullinf[1][j.unit.owner][j.second].append("眼虫茧")
                            elif j.unit_type_name =="OverlordTransport": #如果是取消变眼虫
                                if j.unit.type_history[od].str_id in ['OverseerSiegeModeCocoon','OverlordCocoon']:
                                    Fullinf[0][j.unit.owner][j.second].append("载货王虫")
                                    Fullinf[1][j.unit.owner][j.second].append("眼虫茧")
                                else:
                                    Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                    Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])
                            #统计埋地：以防修改过后出现更多的问题，再次留下修改前的备份：
                                '''
                                else:
                                    #print(j.unit.type_history[od].str_id[-8:])
                                    if j.unit.type_history[od].str_id[-8:]!="Burrowed":
                                        #print("变异单位：{}".format(CClist[j.unit_type_name][0]))
                                        Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                        Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])
                                '''
                            else:
                                #print(j.unit.type_history[od].str_id[-8:])
                                try:
                                    if j.unit.type_history[od].str_id[-8:]!="Burrowed":
                                        #print("变异单位：{}".format(CClist[j.unit_type_name][0]))
                                        Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                        Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])
                                except:
                                    if op==jj:
                                        Fullinf[0][j.unit.owner][j.second].append(CClist[j.unit_type_name][0])
                                        Fullinf[1][j.unit.owner][j.second].append(CClist[j.unit_type_name][1])
                    else:
                        if j.name!='UnitInitEvent' and (j.unit.name in Slist or j.unit.name not in Ilist):
                            if j.name=='UnitDiedEvent':
                                if j.killer:
                                    if j.unit.name=="Archon":
                                        if j.unit.finished_at:
                                            I_UBE[j.unit.owner][j.second].append(Slist[j.unit.name][0])
                                        else:
                                            I_UBE[j.unit.owner][j.second].append("白球(正在融合)")
                                    else:
                                        if j.unit.name in CClist:
                                            #print("变异单位死亡：{}".format(CClist[j.unit.name][0]))
                                            I_UBE[j.unit.owner][j.second].append(CClist[j.unit.name][0])
                                        elif j.unit.name in CCClist:
                                            #print("变异单位死亡：{}".format(CCClist[j.unit.name][0]))
                                            I_UBE[j.unit.owner][j.second].append(CCClist[j.unit.name][0])
                                        else:
                                            if j.unit.finished_at or j.unit.finished_at==0:
                                                I_UBE[j.unit.owner][j.second].append(Slist[j.unit.name][0])
                                else:
                                    if j.unit.name=="DarkTemplar" or j.unit.name=='HighTemplar':
                                        if j.frame not in Ast[j.unit.owner]:
                                            Ast[j.unit.owner][j.frame]=[]
                                        Ast[j.unit.owner][j.frame].append(Slist[j.unit.name][0]) 
                            if j.name=='UnitBornEvent':
                                I_UBE[j.unit.owner][j.second].append(Slist[j.unit.name][0])
            Fullinf.append(I_UBE)

        bar()

        #-------------------------------5.格式化存储------------------------------------------#
        UBE_List={}
        for player in replay.players:
            UBE_List[player]={}
            for Buildevents in Fullinf: #对各类单位事件进行遍历
                for i in Buildevents[player]: #对各类单位事件按参赛者遍历每秒建造列表，i是字典的键
                    if i not in UBE_List[player]: #如果
                        UBE_List[player][i]=[]
                    UBE_List[player][i].append(Buildevents[player][i])
        
        bar()

            #------------------------------6.统计生存单位--------------------------------------#
        Unitalive={name:{} for name in replay.players}
        ua_players={name:{} for name in replay.players}
        for i in UBE_List: #遍历每个选手，i是选手名
            for j in UBE_List[i]: #遍历每秒，j是秒,除了第0秒之外，令当前秒等于上一秒
                if j!=0:
                    Unitalive[i][j]=Unitalive[i][j-1]
                else: 
                    Unitalive[i][j]={}
                for n in range(len(UBE_List[i][j])): #遍历每秒钟的出生项和死亡项,n=0为出生项，n=1为死亡项
                    for nn in UBE_List[i][j][n]:
                        if n==0:
                            #print("{}玩家{}时刻{}出生".format(i,j,nn))
                            if nn not in Unitalive[i][j]:
                                Unitalive[i][j][nn]=0
                            #print(Unitalive[i][j][nn])
                            Unitalive[i][j][nn]+=1
                        if n==1:
                            #print("{}玩家{}时刻{}死亡".format(i,j,nn))
                            try: #如果因为某些原因在存活数量为0时还会死亡单位，就将该单位存活数量设定为0
                                Unitalive[i][j][nn]-=1
                            except:
                                Unitalive[i][j][nn]=0
                            if Unitalive[i][j][nn]==0:
                                del Unitalive[i][j][nn] 
                
                #print(j/1.4//60,j/1.4%60,Unitalive[i][j])
                ua_players[i][j]=list(Unitalive[i][j].items())

        bar()

        #--------------------------7.统计升级列表----------------------------#
        Upgrade_events=a['UpgradeCompleteEvent']
        ue_players={name:{} for name in replay.players}
        res=-1
        for i in Upgrade_events:
            if i.upgrade_type_name!='SprayZerg' and i.upgrade_type_name!='SprayTerran' and i.upgrade_type_name!='SprayProtoss':
                if i.second!=res: 
                    while res!=i.second:
                        res+=1
                        for j in ue_players:
                            ue_players[j][res]=[]
                if i.upgrade_type_name in Ulist and res!=0:
                    if i.player:
                        try:
                            ue_players[i.player][i.second-round(Ulist[i.upgrade_type_name][1]*1.4)].append(Ulist[i.upgrade_type_name][0])
                        except:
                            ue_players[i.player][i.second].append(Ulist[i.upgrade_type_name][0]+"（升级完毕）")
                #else:
                #    ue_players[i.player][i.second].append(i.upgrade_type_name)
        
        bar()
        
        #--------------------------8.统计建筑建造列表----------------------------#
        if 'UnitInitEvent' in a:
            unit_init_events = a['UnitInitEvent']
            uie_players={name:{} for name in replay.players}
            res=-1
            for i in unit_init_events:
                if i.unit.owner:
                    if i.second!=res: 
                        while res!=i.second:
                            res+=1
                            for j in uie_players:
                                uie_players[j][res]=[]
                    if i.unit_type_name in Ilist and res!=0:
                        if i.unit_type_name in Slist:
                            if i.second>=len(ube_players[i.unit.owner]):
                                while len(ube_players[i.unit.owner])-1<=i.second:
                                    n=len(ube_players[i.unit.owner])
                                    ube_players[i.unit.owner][n]=[]
                            ube_players[i.unit.owner][i.second].append(Ilist[i.unit_type_name])
                        else:
                            if (not i.unit.finished_at) and (i.unit.killed_by==i.unit.owner) and i.unit_type_name!='CreepTumorBurrowed' and i.unit_type_name!='CreepTumor':
                                uie_players[i.unit.owner][i.second].append(Ilist[i.unit_type_name]+"（建造后取消）")
                            else: 
                                uie_players[i.unit.owner][i.second].append(Ilist[i.unit_type_name])
                    #else:
                    #    uie_players[i.unit.owner][i.second].append(i.unit.name)

        bar()


        #--------------------------9.统计单位变异列表(目前全部合并到了单位建造和升级科技)----------------------------#
        if 'UnitTypeChangeEvent' in a:
            unit_change_events = a['UnitTypeChangeEvent']
            uce_players={name:{} for name in replay.players}
            res=-1

            for i in unit_change_events:
                if i.unit.owner and i.unit.name!='CreepTumorBurrowed'and i.unit.name!='CreepTumor'  and i.unit.name!='Larva':
                    if i.second!=res: 
                        while res!=i.second:
                            res+=1
                            for j in uce_players:
                                uce_players[j][res]=[]
                    if i.unit_type_name in Clist and res!=0:
                        #如果是虫族升本，就归类到科技升级上去
                        if i.unit_type_name=='Lair':
                            #处理科技升级时长列表长度不够的情况
                            if i.second-80>=len(ue_players[i.unit.owner]):
                                while len(ue_players[i.unit.owner])-1<=i.second-80:
                                    n=len(ue_players[i.unit.owner])
                                    ue_players[i.unit.owner][n]=[]
                            ue_players[i.unit.owner][i.second-80].append(Clist[i.unit_type_name])

                        elif i.unit_type_name in ['Hive','GreaterSpire']:
                            if i.second-99>=len(ue_players[i.unit.owner]):
                                while len(ue_players[i.unit.owner])-1<=i.second-99:
                                    n=len(ue_players[i.unit.owner])
                                    ue_players[i.unit.owner][n]=[]
                            ue_players[i.unit.owner][i.second-99].append(Clist[i.unit_type_name])
                            
                        elif i.unit_type_name =='OrbitalCommand':
                            for f in i.unit.type_history:
                                if i.unit.type_history[f].name=='OrbitalCommand' and f<i.frame:
                                    if i.second>=len(uie_players[i.unit.owner]):
                                        while len(uie_players[i.unit.owner])-1<=i.second:
                                            n=len(uie_players[i.unit.owner])
                                            uie_players[i.unit.owner][n]=[]
                                    #如果这个星轨过去就已经是星轨了！
                                    uie_players[i.unit.owner][i.second].append("星轨落地")
                                    break
                            else:
                                if i.second-35>=len(uie_players[i.unit.owner]):
                                    while len(uie_players[i.unit.owner])-1<=i.second-35:
                                        n=len(uie_players[i.unit.owner])
                                        uie_players[i.unit.owner][n]=[]
                                uie_players[i.unit.owner][i.second-35].append(Clist[i.unit_type_name])

                        elif i.unit_type_name=='PlanetaryFortress':
                            if i.second-50>=len(uie_players[i.unit.owner]):
                                while len(uie_players[i.unit.owner])-1<=i.second-50:
                                    n=len(uie_players[i.unit.owner])
                                    uie_players[i.unit.owner][n]=[]
                            uie_players[i.unit.owner][i.second-50].append(Clist[i.unit_type_name])
                        elif i.unit_type_name in Ilist: #对于剩余的单位变异，只剩下挂件类
                            if i.unit_type_name=='Reactor' or i.unit_type_name=='TechLab':
                                if i.second>=len(uie_players[i.unit.owner]):
                                    while len(uie_players[i.unit.owner])-1<=i.second:
                                        n=len(uie_players[i.unit.owner])
                                        uie_players[i.unit.owner][n]=[]
                                for f in i.unit.type_history:
                                    if f<i.frame:
                                        ff=i.unit.type_history[f].name
                                    else: #当遍历到此刻时，返回上一刻的内容
                                        if ff=='BarracksReactor':
                                            uie_players[i.unit.owner][i.second].append("双倍挂件脱离(兵营)")
                                        if ff=='BarracksTechLab':
                                            uie_players[i.unit.owner][i.second].append("科技挂件脱离(兵营)")
                                        if ff=='FactoryReactor':
                                            uie_players[i.unit.owner][i.second].append("双倍挂件脱离(重工厂)")
                                        if ff=='FactoryTechLab':
                                            uie_players[i.unit.owner][i.second].append("科技挂件脱离(重工厂)")
                                        if ff=='StarportReactor':
                                            uie_players[i.unit.owner][i.second].append("双倍挂件脱离(星港)")
                                        if ff=='StarportTechLab':
                                            uie_players[i.unit.owner][i.second].append("科技挂件脱离(星港)")
                                        break
                            else:
                                if i.second>=len(uie_players[i.unit.owner]):
                                    while len(uie_players[i.unit.owner])-1<=i.second:
                                        n=len(uie_players[i.unit.owner])
                                        uie_players[i.unit.owner][n]=[]
                                uie_players[i.unit.owner][i.second].append(Clist[i.unit_type_name])
                        else:
                            if i.second>=len(ube_players[i.unit.owner]):
                                while len(ube_players[i.unit.owner])-1<=i.second:
                                    n=len(ube_players[i.unit.owner])
                                    ube_players[i.unit.owner][n]=[]
                            ube_players[i.unit.owner][i.second].append(Clist[i.unit_type_name])
                    #else: #顺便列入其他变异项（埋地、由卵变单位等情况）
                        #uce_players[i.unit.owner][i.second].append(i.unit_type_name)

        bar()

        #---------------10.统计人口上限、人口数量、农民数量（测试版-7s更新一次）--------------#
        player_stats_event=a['PlayerStatsEvent']
        pse_players={name:{} for name in replay.players}
        res=-1
        for i in player_stats_event:
            if i.second!=res: 
                while res!=i.second:
                    res+=1
                    for j in pse_players:
                        pse_players[j][res]=[]
            if res!=0:
                pse_players[i.player][i.second].append("{}/{}/{}".format(int(i.food_used),int(i.food_made),int(i.workers_active_count)))

        bar()



        #-------------------------------11.格式化输出------------------------------------------#
        file = open('{}/{}.txt'.format(path,name), 'w',encoding="utf-8")
        DataForPd={}
        PdS=[]
        for i in replay.players:
            file.write("选手{}的建造列表：".format(i)) 
            j=0
            DataForPd[i]=[]
            try:
                if i not in replay.winner:
                    whetherwin="负"
                else:
                    whetherwin="胜"
            except:
                whetherwin="无胜者"
            
            try:
                if i==replay.players[0]:
                    racebattle='{}v{}'.format(replay.players[0].play_race[0],replay.players[1].play_race[0])
                else:
                    racebattle='{}v{}'.format(replay.players[1].play_race[0],replay.players[0].play_race[0])
            except:
                racebattle='{}v{}'.format(replay.players[0].play_race[0],"None")
            PdS.append([re.match('\w{0,}',str(i)[11:]).group(),replay.map_name,i.play_race,racebattle,"{}:{}".format(round(Duration/1.4)//60,round(Duration/1.4)%60),whetherwin,"","","","{}".format(replaypath)])
            while j<Duration:
                #---------------构造DataFrame格式的数据-----------------------------#
                s=[i,"{}:{}".format(round(j/1.4)//60,round(j/1.4)%60)]
                
                #----------------非常混沌的部分-数据整理：遍历各个项目，对重复的计数，对处于同一秒的整合-----------#
                if j<len(pse_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(pse_players[i]) and (pse_players[i][j] or pse_players[i][j+1]):
                        if pse_players[i][j]:
                            cc.append("{}".format(pse_players[i][j][0]))
                        else:
                            cc.append("{}".format(pse_players[i][j+1][0]))
                    else:
                        if pse_players[i][j]:
                            cc.append("{}".format(pse_players[i][j][0]))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")

                if j<len(ua_players[i]):
                    number=""
                    number1=""
                    for n in ua_players[i][j]:
                        if ('工蜂' in n) or('SCV' in n )or ('探姬' in n):
                            number=n[1]
                    cc=[]
                    if j+1<len(ua_players[i]):
                        for n in ua_players[i][j+1]:
                            if ('工蜂' in n) or('SCV' in n )or ('探姬' in n):
                                number1=n[1]

                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(ua_players[i]):
                        cc.append("{}".format(number1))
                    else:
                        cc.append("{}".format(number))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")    

                if j<len(ube_players[i]):
                    cc=[]
                    dd=[]
                    if round((j/1.4))==round(((j+1)/1.4)) and j+1<len(ube_players[i]):
                        dd.append(ube_players[i][j]+ube_players[i][j+1])
                        for c in Counter(ube_players[i][j]+ube_players[i][j+1]):
                            cc.append("{}*{}".format(c,Counter(ube_players[i][j]+ube_players[i][j+1])[c]))
                    else:
                        dd.append(ube_players[i][j])
                        for c in Counter(ube_players[i][j]):
                            cc.append("{}*{}".format(c,Counter(ube_players[i][j])[c]))
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
                if 'UnitInitEvent' in a:
                    if j<len(uie_players[i]):
                        cc=[]
                        dd=[]
                        if round(j/1.4)==round((j+1)/1.4) and j+1<len(uie_players[i]): 
                            for ccc in uie_players[i][j]+uie_players[i][j+1]:                     
                                if ('菌毯' not in ccc) and ("建造后取消" not in ccc) and ("防空管子" not in ccc)  and ("补给站" not in ccc) and ("水晶" not in ccc) and ("起飞" not in ccc) and ("脱离" not in ccc) and ("电池" not in ccc) and ("气矿" not in ccc):
                                    dd.append(ccc)  
                            for c in Counter(uie_players[i][j]+uie_players[i][j+1]):                        
                                cc.append("{}*{}".format(c,Counter(uie_players[i][j]+uie_players[i][j+1])[c]))
                        else:
                            for ccc in uie_players[i][j]:
                                if ('菌毯' not in ccc) and ("建造后取消" not in ccc) and ("防空管子" not in ccc)  and ("补给站" not in ccc) and ("水晶" not in ccc) and ("起飞" not in ccc) and ("脱离" not in ccc) and ("电池" not in ccc) and ("气矿" not in ccc):
                                    dd.append(ccc)
                            for c in Counter(uie_players[i][j]):
                                cc.append("{}*{}".format(c,Counter(uie_players[i][j])[c]))
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

                    
                if j<len(ue_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(ue_players[i]):
                        for c in ue_players[i][j]+ue_players[i][j+1]:
                            cc.append(c)
                    else:
                        for c in ue_players[i][j]:
                            cc.append(c)
                    if cc:
                        s.append(','.join(cc))
                        PdS[-1][6]+=','.join(cc)+','
                    else:
                        s.append('')
                else:
                    s.append("")

                """if j<len(uBe_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(uBe_players[i]):
                        for c in Counter(uBe_players[i][j]+uBe_players[i][j+1]):
                            cc.append("{}*{}".format(c,Counter(uBe_players[i][j]+uBe_players[i][j+1])[c]))
                    else:
                        for c in Counter(uBe_players[i][j]):
                            cc.append("{}*{}".format(c,Counter(uBe_players[i][j])[c]))
                    s.append(cc)
                else:
                    s.append([])"""
                
                if j<len(ua_players[i]):
                    cc=[]
                    if round(j/1.4)==round((j+1)/1.4) and j+1<len(ua_players[i]):
                        cc.append("{}".format(ua_players[i][j+1]))
                    else:
                        cc.append("{}".format(ua_players[i][j]))
                    if cc:
                        s.append(cc[0])
                    else:
                        s.append('')
                else:
                    s.append("")


            


                #-----------------------处理该秒没有发生event的情况-----------------------------#
                tep="\n[{}]".format(s[1])
                if FULLTIME=="FULL":
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

        bar()
        #-------------------------------12.格式化输出excel------------------------------------------#
        for i in DataForPd:
            Inf_to_excel = pd.DataFrame(DataForPd[i],columns=['时间','人口','农民','单位建造','建造建筑','科技升级','当前存活单位'])
            #Inf_to_excel=Inf_to_excel.drop(columns=['index']) #去除某一列
            #print(Inf_to_excel)
            Inf_to_excel.to_excel("{}/{}的建造列表({}).xlsx".format(path,i,name[:-10]),index=False)


        bar()
        return PdS
    except Exception as e:
        global ErrorReport
        ErrorReport+=(name+":\n")
        ErrorReport+=(str(e)+"\n")
        ErrorReport+=("--------------\n")
        print(e)
