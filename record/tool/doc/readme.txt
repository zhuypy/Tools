一、最新部署步骤20190108

	1、解压工具到任意D盘目录
	2、配置conf.properties文件，D:\RE
	3、执行attrib +s +a +h +r D:\RE,确认RE彻底隐藏，执行attrib +s +a +h +r D:\record,确认record彻底隐藏
	4、确认start.bat和startvbs中的执行文件路径
	
	1、新建非管理员用户zhuy,用户组zhuys，将admin和zhuy添加至zhuys组
	2、secpol.msc-本地安全策略-本地策略-用户权限分配-作为批处理作业登录-添加用户或组zhuy
	3、使用admin新建任务计划程序，使用zhuy执行任务

	1、gpedit.msc-用户配置-系统-不运行指定程序taskmgr.exe、cmd.exe、regedit.exe[mmc.exe]
	2、控制面板-系统与安全-防火墙-高级设置-本地计算机上的高级安全windows defender防火墙（左侧目录更目录）-windows defender 防火墙属性，三种类型的出入站全部禁止
	3、新建出站规则：
			允许连接
			作用域：远程IP地址：添加192.168.0.94
	#4、访问192.168.0.94，通；访问192.168.0.93，不通
	#4、尝试打开任务管理器，执行gpedit.msc,启动火狐浏览器

重启登录zhuy
手动输入D：\RE\temp查看录屏文件