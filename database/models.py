# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


class Account(models.Model):
    '''
    对应CTP的账号信息配置
    '''
    # 名称(name)
    name = models.CharField(u'名称',max_length=100)
    # 说明(remarks)
    remarks = models.CharField(u'说明',max_length=500)
    # 交易服务器地址(frontAddress)
    frontAddress = models.CharField(u'交易服务器地址',max_length=100)
    # 行情服务器地址(mdFrontAddress)
    mdFrontAddress = models.CharField(u'行情服务器地址',max_length=100)
    # 代理商编号(brokerID)
    brokerID = models.CharField(u'代理商编号',max_length=50)
    # 用户编号(userID
    userID = models.CharField(u'用户编号',max_length=50)
    # 密码(password)
    password = models.CharField(u'密码',max_length=50)


class Task(models.Model):
    '''
    任务是数据生成器或策略执行器的执行实例，为了逻辑清晰,一个数据生成器或策略执行器只允许有一个执行实例。
    '''
    # 任务类型(type)
    TASK_TYPE = (('DataGenerator', '数据生成器'), ('StrategyExecuter', u'策略执行器'))
    type = models.CharField(u'任务类型', max_length=30,choices=TASK_TYPE)
    # 对应类型配置项(typeRelaId)
    typeRelaId = models.CharField(u'对应的任务配置',max_length=100)
    # 名称(name)
    name = models.CharField(u'名称',max_length=100)
    # 进程标识(pid)
    pid = models.IntegerField(u'进程标识')
    # 启动时间(startTime)
    startTime = models.DateTimeField(u'启动时间', default=datetime.now)
    # 结束时间(endTime)
    endTime = models.DateTimeField(u'结束时间', blank=True, null=True)
    # 状态(state)
    TASK_STATE = ( ('A', u'运行'), ('P', u'停止'))
    state = models.CharField(u'状态', max_length=10,choices=TASK_STATE, default='A')


class TaskLog(models.Model):
    '''
    任务的执行日志
    '''
    # 任务(Task)
    task = models.ForeignKey('Task',verbose_name=u'任务')
    # 日志时间(logTime)
    logTime = models.DateTimeField(u'日志时间', default=datetime.now)
    # 日志信息(logMessage)
    logMessage = models.CharField(u'日志信息',max_length=1000)


class DataCatalog(models.Model):
    '''
    数据目录
    '''
    # 名称(name)
    name = models.CharField(u'名称',max_length=100)
    # 说明(remarks)
    remarks = models.CharField(u'说明',max_length=500)



class DepthMarketData(models.Model):
    '''
    深度行情数据存储(对应CTP数据结构CThostFtdcDepthMarketDataField)
    '''
    # 所属的目录(catalog)
    dataCatalog = models.ForeignKey('DataCatalog',verbose_name=u'所属数据目录')
    # 数据时间(相当于TradingDay+UpdateTime+UpdateMillisec)
    dataTime = models.DateTimeField(u'数据时间')

    # CThostFtdcDepthMarketDataField 字段定义
    TradingDay = models.CharField(u'交易日', max_length=9, default='')
    InstrumentID = models.CharField(u'合约代码', max_length=31, default='')
    ExchangeID = models.CharField(u'交易所代码', max_length=9, default='')
    ExchangeInstID = models.CharField(u'合约在交易所的代码', max_length=31, default='')
    LastPrice = models.FloatField(u'最新价', default=0)
    PreSettlementPrice = models.FloatField(u'上次结算价', default=0)
    PreClosePrice = models.FloatField(u'昨收盘', default=0)
    PreOpenInterest = models.FloatField(u'昨持仓量', default=0)
    OpenPrice = models.FloatField(u'今开盘', default=0)
    HighestPrice = models.FloatField(u'最高价', default=0)
    LowestPrice = models.FloatField(u'最低价', default=0)
    Volume = models.IntegerField(u'数量', default=0)
    Turnover = models.FloatField(u'成交金额', default=0)
    OpenInterest = models.FloatField(u'持仓量', default=0)
    ClosePrice = models.FloatField(u'今收盘', default=0)
    SettlementPrice = models.FloatField(u'本次结算价', default=0)
    UpperLimitPrice = models.FloatField(u'涨停板价', default=0)
    LowerLimitPrice = models.FloatField(u'跌停板价', default=0)
    PreDelta = models.FloatField(u'昨虚实度', default=0)
    CurrDelta = models.FloatField(u'今虚实度', default=0)
    UpdateTime = models.CharField(u'最后修改时间', max_length=9, default='')
    UpdateMillisec = models.IntegerField(u'最后修改毫秒', default=0)
    BidPrice1 = models.FloatField(u'申买价一', default=0)
    BidVolume1 = models.IntegerField(u'申买量一', default=0)
    AskPrice1 = models.FloatField(u'申卖价一', default=0)
    AskVolume1 = models.IntegerField(u'申卖量一', default=0)
    BidPrice2 = models.FloatField(u'申买价二', default=0)
    BidVolume2 = models.IntegerField(u'申买量二', default=0)
    AskPrice2 = models.FloatField(u'申卖价二', default=0)
    AskVolume2 = models.IntegerField(u'申卖量二', default=0)
    BidPrice3 = models.FloatField(u'申买价三', default=0)
    BidVolume3 = models.IntegerField(u'申买量三', default=0)
    AskPrice3 = models.FloatField(u'申卖价三', default=0)
    AskVolume3 = models.IntegerField(u'申卖量三', default=0)
    BidPrice4 = models.FloatField(u'申买价四', default=0)
    BidVolume4 = models.IntegerField(u'申买量四', default=0)
    AskPrice4 = models.FloatField(u'申卖价四', default=0)
    AskVolume4 = models.IntegerField(u'申卖量四', default=0)
    BidPrice5 = models.FloatField(u'申买价五', default=0)
    BidVolume5 = models.IntegerField(u'申买量五', default=0)
    AskPrice5 = models.FloatField(u'申卖价五', default=0)
    AskVolume5 = models.IntegerField(u'申卖量五', default=0)
    AveragePrice = models.FloatField(u'当日均价', default=0)
    ActionDay = models.CharField(u'业务日期', max_length=9, default='')

    class Meta:
        ordering = ['-TradingDay','-UpdateTime','-UpdateMillisec']


class DataGenerator(models.Model):
    '''
    数据生成器配置
    '''
    # 名称(name)
    name = models.CharField(u'名称',max_length=100)
    # 账号(account)
    account = models.ForeignKey('Account',verbose_name=u'账号')
    # 所属的目录(dataCatalog)
    dataCatalog = models.ForeignKey('DataCatalog',verbose_name=u'所属数据目录')
    # 数据源(dataSource)
    DATA_SOURCE_TYPE = (('Channel',u'CTP接口'),('Database',u'数据库'))
    dataSource = models.CharField(u'数据源', max_length=30,choices=DATA_SOURCE_TYPE)
    # 数据起始时间(datetimeBegin)
    datetimeBegin = models.DateTimeField(u'数据起始时间',blank=True, null=True)
    # 数据结束时间(datetimeEnd)
    datetimeEnd = models.DateTimeField(u'数据结束时间',blank=True, null=True)
    # 品种列表(instrumentIDList)
    instrumentIDList = models.CharField(u'品种列表',max_length=500)
    # 是否保存原始数据流(saveRawData)
    saveRawData = models.BooleanField('是否保存原始数据流',default=False)
    # 是否保存棒线数据(saveBarData)
    saveBarData = models.BooleanField('是否保存棒线数据',default=False)
    # 是否保存指标数据(saveIndexData)
    saveIndexData = models.BooleanField('是否保存指标数据',default=False)
    # 数据广播地址(broadcastAddress)
    broadcastAddress = models.CharField(u'数据广播地址',max_length=100)


class StrategyExecuter(models.Model):
    '''
    策略执行器
    '''
    # 名称(name)
    name = models.CharField(u'名称',max_length=100)
    # 账号(account)
    account = models.ForeignKey('Account',verbose_name=u'账号')
    # 策略程序所在目录(strategyDir)
    strategyDir = models.CharField(u'策略程序所在目录',max_length=500)
    # 策略程序名称(strategyProgram)
    strategyProgram = models.CharField(u'策略程序名称',max_length=100)
    # 策略配置文件(strategyConfig)
    strategyConfig = models.CharField(u'策略配置文件',max_length=100)
    # 数据接收地址(receiveAddress)
    receiveAddress = models.CharField(u'数据接收地址',max_length=100)
    # 品种列表(instrumentIDList)
    instrumentIDList = models.CharField(u'品种列表',max_length=500)
    # 默认头寸大小(volume)
    volume = models.FloatField(u'默认头寸大小', default=1)
    # 最大做多头寸数量(maxBuyPosition)
    maxBuyPosition = models.IntegerField(u'最大做多头寸数量', default=1)
    # 最大做空头寸数量(maxSellPosition)
    maxSellPosition = models.IntegerField(u'最大做多头寸数量', default=1)


class TradingRecord(models.Model):
    '''
    交易记录
    '''
    # 任务(task)
    task = models.ForeignKey('Task',verbose_name=u'任务')
    # 策略执行器(strategyExecuter)
    strategyExecuter = models.ForeignKey('StrategyExecuter',verbose_name=u'策略执行器')
    # 头寸标识(positionId)
    # 品种(instrumentID)
    instrumentID = models.CharField(u'品种',max_length=50)
    # 交易方向(tradingDirection)
    TRADING_DIRECTION = (('Buy',u'做多'),('Sell',u'做空'))
    tradingDirection = models.CharField(u'交易方向', max_length=30,choices=TRADING_DIRECTION)
    # 交易数量(volume)
    volume = models.FloatField(u'交易数量')
    # 开仓价格(openPrice)
    openPrice = models.FloatField(u'开仓价格')
    # 平仓价格(closePrice)
    closePrice = models.FloatField(u'平仓价格')
    # 状态(state)
    TRADING_STATE = (('Open',u'开仓'),('Close',u'平仓'))
    state = models.CharField(u'状态', max_length=30,choices=TRADING_STATE)