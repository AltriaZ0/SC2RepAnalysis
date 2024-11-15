#--------------------------2.需要用到的数据：建造时间、变异后单位和升级时间----------------------------#
Slist={'SCV':["SCV",12],'MULE':["矿骡",0],
    'Marine':["枪兵",18],'Reaper':["死神",32],'Marauder':["光头",21],'Ghost':["鬼兵",29],
    'Hellion':["火车",21],'WidowMine':["地雷",21],'WidowMineBurrowed':["地雷",21],'Cyclone':["导弹车",32],'SiegeTank':["坦克",32],'SiegeTankSieged':["坦克",32],'BattleHellion':["火车侠？",21],'Thor':["雷神",43],'ThorAP':["雷神",43],
    'Viking':["维京",30],'Medivac':["运输机",30],'Liberator':["解放者",43],'LiberatorAG':["解放者",43],'Raven':["渡鸦",34],'Banshee':["女妖",43],'Battlecruiser':["战列巡航舰",64],
    #----------------------------------------------#
    'Probe':["探姬",12],'Adept':["使徒",30],'Sentry':["哨兵",23],'Zealot':["叉叉",27],'Stalker':["追猎",30],'HighTemplar':["闪电",39],'DarkTemplar':["隐刀",39],'Archon':["白球",8.57],'Observer':["叮当(ob)",21],'ObserverSiegeMode':["叮当(ob)",21],'WarpPrism':["棱镜",36],
    'Immortal':["不朽",39],'Colossus':["巨像",54],'Disruptor':["自爆球",36], 'Phoenix':["凤凰",25],'VoidRay':["虚空辉光舰",43],'Oracle':["先知",37],'Tempest':["风暴",43],'Carrier':["航母",64],
    #'Interceptor':["航母小飞机",9],
    'Mothership':["母舰",79],
    #----------------------------------------------#
    'Drone':["工蜂",12],'DroneBurrowed':["农民",12],
    'Zergling':["小狗",17],'ZerglingBurrowed':["小狗",17],'Baneling':["小狗",17],'BanelingBurrowed':["小狗",17],
    'Roach':["蟑螂",19],'Ravager':["蟑螂",19],'RoachBurrowed':["蟑螂",19],'RavagerBurrowed':["蟑螂",19],'RavagerCocoon':["蟑螂",19],
    'Queen':["女王",36],'QueenBurrowed':["女王",36],
    'Hydralisk':["刺蛇",24],'HydraliskBurrowed':["刺蛇",24],'Lurker':["刺蛇",24],'LurkerBurrowed':["刺蛇",24],
    'Infestor':["感染虫",36],'InfestorBurrowed':["感染虫",36],
    'Ultralisk':["大牛",39],'UltraliskBurrowed':["大牛",39],
    'SwarmHost':["宿主",29],'SwarmHostBurrowed':["宿主",29],
    'Overlord':["房子",18],'Overseer':["房子",18],'OverseerSiegeMode':["房子",18],'OverlordTransport':["房子",18],
    'Egg':["夭折的卵",0],
    'Corruptor':["腐化",29],'BroodLord':["腐化",29],
    'Changeling':["拟态虫",0],'ChangelingMarine':["拟态枪兵",0],'ChangelingZealot':["拟态叉叉",0],'ChangelingZergling':["拟态狗狗",0],
    'CreepTumorQueen*1':["夭折的菌毯",0],
    'Mutalisk':["飞龙",24],
    'Viper':["飞蛇",29],
    'LocustMPFlying':["宿主小虫子起飞",0],
    # 'Locust':["宿主小虫子：飞翔",0],'LocustMPPrecursor':["宿主小虫子：落地",0]
    }
Clist={'BanelingCocoon':"毒爆",'RavagerCocoon':"火蟑螂",'LurkerMPEgg':"地刺",
    'Hive':"三本",'Lair':"二本",
    'OrbitalCommand':"星轨",'PlanetaryFortress':"要塞",'CommandCenterFlying':"指挥中心起飞",'CommandCenter':"指挥中心落地",'OrbitalCommandFlying':"星轨起飞",'FactoryFlying':"重工厂起飞",'StarportFlying':"星港起飞",'BarracksFlying':"兵营起飞",'Factory':"重工厂落地",'Barracks':"兵营落地",'Starport':"星港落地",
    'BarracksReactor':"接入双倍挂件(兵营)",'BarracksTechLab':"接入科技挂件(兵营)",'StarportTechLab':"接入科技挂件(星港)",'StarportReactor':"接入双倍挂件(星港)",'FactoryReactor':"接入双倍挂件(重工厂)",'FactoryTechLab':"接入科技挂件(重工厂)",'Reactor':"双倍挂件脱离",'TechLab':"科技挂件脱离",
    'GreaterSpire':"大龙塔",
    'BroodLordCocoon':"大龙",
        'TransportOverlordCocoon':"载货王虫",'OverseerSiegeModeCocoon':"眼虫",'OverlordCocoon':"眼虫"
        }
CClist={'Baneling':["毒爆","毒爆卵"],'Ravager':["火蟑螂","火蟑螂茧"],'LurkerMP':["地刺","地刺茧"],'Lurker':["地刺","地刺茧"], 'BroodLord':["大龙","大龙茧"],'OverlordTransport':["载货王虫",'载货王虫茧'],'Overseer':["眼虫","眼虫茧"],
        'BroodLordCocoon':["大龙茧","腐化"],'TransportOverlordCocoon':["载货王虫茧","房子"],'OverseerSiegeModeCocoon':["眼虫茧","房子"],'OverlordCocoon':["眼虫茧","房子"],'BanelingCocoon':["毒爆卵","小狗"],'RavagerCocoon':["火蟑螂茧",'蟑螂'],'LurkerMPEgg':["地刺茧","刺蛇"],
        'Zergling':["小狗","毒爆卵"],'Roach':["蟑螂","火蟑螂茧"],'Hydralisk':["刺蛇","地刺茧"],'Corruptor':["腐化","大龙茧"]}
CCClist={'BanelingBurrowed':["毒爆","小狗"],'RavagerBurrowed':["火蟑螂","蟑螂"],'Lurker':["地刺","刺蛇"],'LurkerBurrowed':["地刺","刺蛇"]
        }
Ilist={'Hatchery':"孵化场",'Extractor':"气矿",'SpawningPool':"血池",
    'SporeCrawler':"防空管子",'SporeCrawlerUprooted':"防空管子",
    'SpineCrawler':"对地管子",'SpineCrawlerUprooted':"对地管子",
    'ExtractorRich':"高能瓦斯",
    'CreepTumorBurrowed':"菌毯",'CreepTumor':"菌毯",'CreepTumorQueen':"菌毯",
    'BanelingNest':"毒爆虫巢",'EvolutionChamber':"进化腔(BV)",'RoachWarren':"蟑螂巢",
    'GreaterSpire':"龙塔",'Lair':"孵化场",'Hive':"孵化场",'InfestationPit':"感染深渊",'Spire':"龙塔",
    'NydusNetwork':"虫道网络",'NydusCanal':"虫洞",'LurkerDenMP':"地刺巢",'LurkerDen':"地刺巢",
    'UltraliskCavern':"牛牛巢穴",'HydraliskDen':"刺蛇巢",
    #------------------------------------------------------------------------#
    'Pylon':"水晶",'WarpGate':"传送门",'Gateway':"传送门",'Assimilator':"气矿",'Nexus':"星灵枢纽",'CyberneticsCore':"控制芯核(BY)",'TwilightCouncil':"光影议会(VC)",'RoboticsFacility':"机械台(VR)",'RoboticsBay':"机械研究所(VB)",'TemplarArchive':'圣堂武士文献馆(VT)','ShieldBattery':'电池','Stargate':'星门','Forge':'锻炉(BF)','FleetBeacon':'舰队航标(VF)','DarkShrine':"隐刀塔(VD)",'PhotonCannon':"地堡",
    'Adept':"使徒",'Sentry':"哨兵",'Zealot':"叉叉",'Stalker':"追猎",'HighTemplar':"闪电",'DarkTemplar':"隐刀",'Archon':"白球",
    #-------------------------------------------------------------------------#
    'MissileTurret':"导弹塔","SensorTower":"感应塔",'SupplyDepot':"补给站",'SupplyDepotLowered':"补给站",
    'Barracks':"兵营","Factory":"重工厂(VF)",'Starport':"星港(VS)",'OrbitalCommandFlying':"星轨起飞",'FactoryFlying':"重工厂起飞",'StarporFlying':"星港起飞",'BarracksFlying':"兵营起飞",
    "Refinery":"气矿","Armory":"军械库(VA)",'EngineeringBay':"工程站(BE)",
    'GhostAcademy':"幽灵军校",'FusionCore':"大和巢穴",
    'BarracksReactor':"新建双倍挂件(兵营)",'BarracksTechLab':"新建科技挂件(兵营)",'StarportTechLab':"新建科技挂件(星港)",'StarportReactor':"新建双倍挂件(星港)",'FactoryReactor':"新建双倍挂件(重工厂)",'FactoryTechLab':"新建科技挂件(重工厂)",'Reactor':"双倍挂件",'TechLab':"科技挂件",
    'OrbitalCommand':"基地",'PlanetaryFortress':"基地",'CommandCenter':"基地",'Bunker':"地堡",
    }
Ulist={'zerglingmovementspeed':["狗速",79],'zerglingattackspeed':["狂狗",93],
    'Burrow':["埋地",71],'overlordspeed':["房子速度",43],
    'ZergMeleeWeaponsLevel1':["近战一攻",114],'ZergMeleeWeaponsLevel2':["近战两攻",136],'ZergMeleeWeaponsLevel3':["近战三攻",157],
    'ZergMissileWeaponsLevel1':["远程一攻",114],'ZergMissileWeaponsLevel2':["远程两攻",136],'ZergMissileWeaponsLevel3':["远程三攻",157],
        'ZergGroundArmorsLevel1':["地面一甲",114],'ZergGroundArmorsLevel2':["地面两甲",136],'ZergGroundArmorsLevel3':["地面三甲",157],
        'ZergFlyerWeaponsLevel1':["空军一攻",114],'ZergFlyerWeaponsLevel2':["空军两攻",136],'ZergFlyerWeaponsLevel3':["空军三攻",157],
        'ZergFlyerArmorsLevel1':["空军一防",114],'ZergFlyerArmorsLevel2':["空军两防",136],'ZergFlyerArmorsLevel3':["空军三防",157],                 
    'GlialReconstitution':["蟑螂速度",79],'TunnelingClaws':["蟑螂埋地移动",79],
    'CentrificalHooks':["毒爆速度",71],
    'NeuralParasite':["感染控",79],
        'EvolveMuscularAugments':["刺蛇速度",64],'EvolveGroovedSpines':["刺蛇射程",50],
        'DiggingClaws':["地刺速埋",57],'LurkerRange':["地刺射程",57],
        'ChitinousPlating':["牛甲",79],'AnabolicSynthesis':["牛牛喷气背包",43],
        #--------------------------------------------------------------------------------------------#
        'TerranBuildingArmor':["建筑甲",100],'HiSecAutoTracking':["建筑射程",57],
        'PunisherGrenades':["震撼弹",43],'ShieldWall':["盾牌",79],'Stimpack':["兴奋剂",100],
        'BansheeCloak':["女妖隐形",79],'InterferenceMatrix':["渡鸦锁定",57],'LiberatorAGRangeUpgrade':["解放射程",79],'BansheeSpeed':["女妖速度",100],
        'PersonalCloaking':["鬼兵隐形",86],
        'HurricaneThrusters':["导弹车速度",100],'DrillClaws':["地雷速埋",79],'SmartServos':["快速变形",79],'HighCapacityBarrels':["蓝火",79],
        'BattlecruiserEnableSpecializations':["大和炮",100],'MedivacCaduceusReactor':["运输机回能速度",53],
        'TerranInfantryWeaponsLevel1':["生化一攻",114],'TerranInfantryArmorsLevel1':["生化一防",114],'TerranVehicleAndShipArmorsLevel1':["机械化一防",114],'TerranShipWeaponsLevel1':["空军一攻",114],'TerranVehicleWeaponsLevel1':["机械化一攻",114],
        'TerranInfantryWeaponsLevel2':["生化两攻",136],'TerranInfantryArmorsLevel2':["生化两防",136],'TerranVehicleAndShipArmorsLevel2':["机械化两防",136],'TerranShipWeaponsLevel2':["空军两攻",136],'TerranVehicleWeaponsLevel2':["机械化两攻",136],
        'TerranInfantryWeaponsLevel3':["生化三攻",157],'TerranInfantryArmorsLevel3':["生化三防",157],'TerranVehicleAndShipArmorsLevel3':["机械化三防",157],'TerranShipWeaponsLevel3':["空军三攻",157],'TerranVehicleWeaponsLevel3':["机械化三攻",157],
        #----------------------------------------------------------------------------------------------#
        'WarpGateResearch':["折跃门",100],'BlinkTech':["追猎闪烁",100],'ResonatingGlaives':["使徒攻速",100],'Charge':["叉叉脚速",100],'ExtendedThermalLance':['巨像射程',100],'PsiStormTech':['闪电科技',79],'GraviticDrive':["提速棱镜",57],
        'DarkTemplarBlinkUpgrade':["隐刀闪烁",100],
        'TempestGroundAttackUpgrade':['风暴对建筑伤害',100],'PhoenixRangeUpgrade':["凤凰射程",64],'VoidRaySpeedUpgrade':["虚空速度",80],
        'ObserverGraviticBooster':['提速OB',80],
        'ProtossAirWeaponsLevel1':["空军一攻",129],'ProtossGroundWeaponsLevel1':["地面一攻",129],'ProtossShieldsLevel1':['一级护盾',129],'ProtossAirArmorsLevel1':['空军一防',129],'ProtossGroundArmorsLevel1':['地面一防',129],
        'ProtossAirWeaponsLevel2':["空军两攻",154],'ProtossGroundWeaponsLevel2':["地面二攻",154],'ProtossShieldsLevel2':['两级护盾',154],'ProtossAirArmorsLevel2':['空军两防',154],'ProtossGroundArmorsLevel2':['地面两防',154],
        'ProtossAirWeaponsLevel3':["空军三攻",179],'ProtossGroundWeaponsLevel3':["地面三攻",179],'ProtossShieldsLevel3':['三级护盾',179],'ProtossAirArmorsLevel3':['空军三防',179],'ProtossGroundArmorsLevel3':['地面三防',179],
}