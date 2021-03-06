#!/usr/bin/env python
# encoding: utf-8

from comhelper import setDjangoEnvironment
setDjangoEnvironment()

from database.models import *
from datetime import datetime
from pyctp.CTPChannel import TraderChannel
from pyctp.CTPChannel import CThostFtdcInputOrderField
from pyctp.CTPChannel import CThostFtdcSettlementInfoConfirmField

UnkownPositionDirection = [-3000,u'未知头寸方向',None]
PositionNotExists = [-3001,u'头寸不存在',None]
PositionNotInOpenState = [-3002,u'头寸不处于打开状态',None]

class Trader(object):
    '''
    交易处理类
    '''

    def __init__(self,account,task=None,strategyExecuter=None,simulate=False):
        '''
        构造函数
        traderChannel CTP Trader 交易通道的实例
        task 对应的任务数据对象(database.models.ModelTask)
        strategyExecuter 策略执行器数据对象(database.models.ModelStrategyExecuter)
        '''
        self.task = task
        self.strategyExecuter = strategyExecuter
        self.simulate = simulate
        self.brokerID = account.brokerID
        self.userID = account.userID
        self.traderChannel = TraderChannel(
            account.frontAddress,
            account.brokerID,
            account.userID,
            account.password
        )
        self.orderRefSeq = 0

        # 确认交易信息
        self.settlementInfoConfirm()


    def settlementInfoConfirm(self):
        # 确认交易记录
        requestData = CThostFtdcSettlementInfoConfirmField()
        requestData.BrokerID = self.brokerID
        requestData.InvestorID = self.userID
        result = self.traderChannel.SettlementInfoConfirm(requestData)
        if result[0] <> 0:
            raise Exception(u'确认之前交易信息失败')


    def getTraderChannel(self):
        '''
        读取当前交易对象的交易通道
        '''
        return self.traderChannel


    def getOrderRef(self,orderId):
        '''
        获取OrderRef序列值
        '''
        return ('%12d' % orderId).replace(' ','0') # '000000000001'


    def getSimulate(self):
        '''
        '''
        return self.simulate


    def orderInsert(self,orderRef,instrumentID,orderPriceType = '1',direction = '0',combOffsetFlag = '0',
            combHedgeFlag = '1',limitPrice = 0,volumeTotalOriginal = 1,timeCondition = '1',gTDDate = '',
            volumeCondition = '1',minVolume = None,contingentCondition = '1',stopPrice = 0,forceCloseReason = '0',
            isAutoSuspend = 0,businessUnit = '',requestID = 1,userForceClose = 0,isSwapOrder = 0):
        '''
        orderRef 报单序列号实际就是数据对象ModelPosition的id转化为字符串
        instrumentID 交易品种代码
        orderPriceType 报单价格条件 char
        //// THOST_FTDC_OPT_AnyPrice '1' 任意价
        //// THOST_FTDC_OPT_LimitPrice '2' 限价
        //// THOST_FTDC_OPT_BestPrice '3' 最优价
        //// THOST_FTDC_OPT_LastPrice '4' 最新价
        //// THOST_FTDC_OPT_LastPricePlusOneTicks '5' 最新价浮动上浮1个ticks
        //// THOST_FTDC_OPT_LastPricePlusTwoTicks '6' 最新价浮动上浮2个ticks
        //// THOST_FTDC_OPT_LastPricePlusThreeTicks '7' 最新价浮动上浮3个ticks
        //// THOST_FTDC_OPT_AskPrice1 '8' 卖一价
        //// THOST_FTDC_OPT_AskPrice1PlusOneTicks '9' 卖一价浮动上浮1个ticks
        //// THOST_FTDC_OPT_AskPrice1PlusTwoTicks 'A' 卖一价浮动上浮2个ticks
        //// THOST_FTDC_OPT_AskPrice1PlusThreeTicks 'B' 卖一价浮动上浮3个ticks
        //// THOST_FTDC_OPT_BidPrice1 'C' 买一价
        //// THOST_FTDC_OPT_BidPrice1PlusOneTicks 'D' 买一价浮动上浮1个ticks
        //// THOST_FTDC_OPT_BidPrice1PlusTwoTicks 'E' 买一价浮动上浮2个ticks
        //// THOST_FTDC_OPT_BidPrice1PlusThreeTicks 'F' 买一价浮动上浮3个ticks
        direction 买卖方向 char
        //// THOST_FTDC_D_Buy '0' 买
        //// THOST_FTDC_D_Sell '1' 卖
        combOffsetFlag 组合开平标志 char[5]
        //// THOST_FTDC_OF_Open '0' 开仓
        //// THOST_FTDC_OF_Close '1' 平仓
        //// THOST_FTDC_OF_ForceClose '2' 强平
        //// THOST_FTDC_OF_CloseToday '3' 平今
        //// THOST_FTDC_OF_CloseYesterday '4' 平昨
        //// THOST_FTDC_OF_ForceOff '5' 强减
        //// THOST_FTDC_OF_LocalForceClose '6' 本地强平
        combHedgeFlag 组合投机套保标志 char[5]
        //// THOST_FTDC_HF_Speculation '1' 投机
        //// THOST_FTDC_HF_Arbitrage '2' 套利
        //// THOST_FTDC_HF_Hedge '3' 套保
        limitPrice 价格 double
        volumeTotalOriginal 数量 int
        timeCondition 有效期类型 char
        //// THOST_FTDC_TC_IOC '1' 立即完成，否则撤销
        //// THOST_FTDC_TC_GFS '2' 本节有效
        //// THOST_FTDC_TC_GFD '3' 当日有效
        //// THOST_FTDC_TC_GTD '4' 指定日期前有效
        //// THOST_FTDC_TC_GTC '5' 撤销前有效
        //// THOST_FTDC_TC_GFA '6' 集合竞价有效
        gTDDate GTD日期 char[9]
        volumeCondition 成交量类型 char
        //// THOST_FTDC_VC_AV '1' 任何数量
        //// THOST_FTDC_VC_MV '2' 最小数量
        //// THOST_FTDC_VC_CV '3' 全部数量
        minVolume 最小成交量 int
        contingentCondition 触发条件 char
        //// THOST_FTDC_CC_Immediately '1' 立即
        //// THOST_FTDC_CC_Touch '2' 止损
        //// THOST_FTDC_CC_TouchProfit '3' 止盈
        //// THOST_FTDC_CC_ParkedOrder '4' 预埋单
        //// THOST_FTDC_CC_LastPriceGreaterThanStopPrice '5' 最新价大于条件价
        //// THOST_FTDC_CC_LastPriceGreaterEqualStopPrice '6' 最新价大于等于条件价
        //// THOST_FTDC_CC_LastPriceLesserThanStopPrice '7' 最新价小于条件价
        //// THOST_FTDC_CC_LastPriceLesserEqualStopPrice '8' 最新价小于等于条件价
        //// THOST_FTDC_CC_AskPriceGreaterThanStopPrice '9' 卖一价大于条件价
        //// THOST_FTDC_CC_AskPriceGreaterEqualStopPrice 'A' 卖一价大于等于条件价
        //// THOST_FTDC_CC_AskPriceLesserThanStopPrice 'B' 卖一价小于条件价
        //// THOST_FTDC_CC_AskPriceLesserEqualStopPrice 'C' 卖一价小于等于条件价
        //// THOST_FTDC_CC_BidPriceGreaterThanStopPrice 'D' 买一价大于条件价
        //// THOST_FTDC_CC_BidPriceGreaterEqualStopPrice 'E' 买一价大于等于条件价
        //// THOST_FTDC_CC_BidPriceLesserThanStopPrice 'F' 买一价小于条件价
        //// THOST_FTDC_CC_BidPriceLesserEqualStopPrice 'H' 买一价小于等于条件价
        stopPrice 止损价 double
        forceCloseReason 强平原因 char
        //// THOST_FTDC_CC_Immediately '1' 立即
        //// THOST_FTDC_CC_Touch '2' 止损
        //// THOST_FTDC_CC_TouchProfit '3' 止盈
        //// THOST_FTDC_CC_ParkedOrder '4' 预埋单
        //// THOST_FTDC_CC_LastPriceGreaterThanStopPrice '5' 最新价大于条件价
        //// THOST_FTDC_CC_LastPriceGreaterEqualStopPrice '6' 最新价大于等于条件价
        //// THOST_FTDC_CC_LastPriceLesserThanStopPrice '7' 最新价小于条件价
        //// THOST_FTDC_CC_LastPriceLesserEqualStopPrice '8' 最新价小于等于条件价
        //// THOST_FTDC_CC_AskPriceGreaterThanStopPrice '9' 卖一价大于条件价
        //// THOST_FTDC_CC_AskPriceGreaterEqualStopPrice 'A' 卖一价大于等于条件价
        //// THOST_FTDC_CC_AskPriceLesserThanStopPrice 'B' 卖一价小于条件价
        //// THOST_FTDC_CC_AskPriceLesserEqualStopPrice 'C' 卖一价小于等于条件价
        //// THOST_FTDC_CC_BidPriceGreaterThanStopPrice 'D' 买一价大于条件价
        //// THOST_FTDC_CC_BidPriceGreaterEqualStopPrice 'E' 买一价大于等于条件价
        //// THOST_FTDC_CC_BidPriceLesserThanStopPrice 'F' 买一价小于条件价
        //// THOST_FTDC_CC_BidPriceLesserEqualStopPrice 'H' 买一价小于等于条件价
        isAutoSuspend 自动挂起标志 int
        businessUnit 业务单元 char[21]
        requestID 请求编号 int
        userForceClose 用户强评标志 int
        isSwapOrder 互换单标志 int
        '''
        requestData = CThostFtdcInputOrderField()
        requestData.BrokerID = self.brokerID
        requestData.InvestorID = self.userID
        requestData.InstrumentID = instrumentID
        requestData.OrderRef = orderRef
        requestData.UserID = self.userID
        requestData.OrderPriceType = orderPriceType
        requestData.Direction = direction
        requestData.CombOffsetFlag = combOffsetFlag
        requestData.CombHedgeFlag = combHedgeFlag
        requestData.LimitPrice = limitPrice
        requestData.VolumeTotalOriginal = volumeTotalOriginal
        requestData.TimeCondition = timeCondition
        requestData.GTDDate = gTDDate
        requestData.VolumeCondition = volumeCondition
        requestData.MinVolume = minVolume or volumeTotalOriginal
        requestData.ContingentCondition = contingentCondition
        requestData.StopPrice = stopPrice
        requestData.ForceCloseReason = forceCloseReason
        requestData.IsAutoSuspend = isAutoSuspend
        requestData.BusinessUnit = businessUnit
        requestData.RequestID = requestID
        requestData.UserForceClose = userForceClose
        requestData.IsSwapOrder = isSwapOrder

        result = self.traderChannel.OrderInsert(requestData)
        return result



    def open(self,instrumentID,directionCode,volume=None):
        '''
        创建头寸,使用现价开仓
        instrumentID   交易品种代码
        directionCode    头寸方向: 'buy' 做多，'sell' 做空
        volume  交易手数,如果为空尝试使用策略执行器配置，如果策略执行器也无指定,默认为1
        '''

        # 转换头寸方向参数
        if directionCode == 'buy' :
            direction = '0'
        elif directionCode == 'sell':
            direction = '1'
        else:
            return UnkownPositionDirection

        # 设置头寸大小
        if volume == None :
            if self.strategyExecuter != None:
                volumeTotalOriginal = self.strategyExecuter.None or 1
            else:
                 volumeTotalOriginal = 1
        else:
            volumeTotalOriginal = volume

        # 创建报单记录
        order = ModelOrder()
        order.task = self.task
        order.strategyExecuter = self.strategyExecuter
        order.simulate = self.simulate
        order.instrumentID = instrumentID
        order.action = 'open'
        order.directionCode = directionCode
        order.volume = volumeTotalOriginal
        order.price = 0   # 任意价
        order.priceCondition = 'immediate'
        order.insertTime = datetime.now()
        order.state = 'insert'
        order.errorId = 0
        order.errorMsg = ''
        order.save()
        order.orderRef = self.getOrderRef(order.id)
        order.save()


        # 发送建单请求
        errorId,errorMsg,data = self.orderInsert(
            instrumentID = instrumentID,
            orderRef = order.orderRef,
            direction = direction,
            combOffsetFlag = '0',     #开仓
            volumeTotalOriginal = volumeTotalOriginal
        )

        if errorId == 0 :
            # 生成头寸记录
            position = ModelPosition()
            position.task = self.task
            position.strategyExecuter = self.strategyExecuter
            position.simulate = self.simulate
            position.instrumentID = instrumentID
            position.directionCode = directionCode
            position.volume = volumeTotalOriginal
            position.openTime = datetime.now()
            position.state = 'open'
            position.openPrice = data[0].Price
            position.save()

            # 更新报单信息
            order.state = 'finish'
            order.finishTime = datetime.now()
            order.price = data[0].Price
            order.save()

            # 返回成功
            return 0,u'',position
        else:
            order.state = 'error'
            order.finishTime = datetime.now()
            order.errorId = errorId
            order.errorMsg = errorMsg
            order.save()
            return errorId,errorMsg,None


    def close(self,positionId):
        '''
        关闭头寸,使用现价平仓
        positionId  对应的头寸记录的Id
        '''
        # 读取ModelPosition记录
        try:
            position = ModelPosition.objects.get(id=positionId)
        except:
            return PositionNotExists

        # 检查头寸是否处于打开状态
        if position.state not in ('open'):
            return PositionNotInOpenState

        # 生成关闭头寸的报单
        order = ModelOrder()
        order.task = self.task
        order.strategyExecuter = self.strategyExecuter
        order.simulate = self.simulate
        order.position = position
        order.instrumentID = position.instrumentID
        order.action = 'close'
        order.directionCode = position.directionCode
        order.volume = position.volume
        order.price = 0    # 现价平
        order.priceCondition = 'immediate'
        order.insertTime = datetime.now()
        order.state = 'insert'
        order.errorId = 0
        order.errorMsg = ''
        order.save()   # 生成order.id
        order.orderRef = self.getOrderRef(order.id)
        order.save()

        # 转换头寸方向参数
        # NOTE:注意ctp平仓时交易方向是相反的
        if position.directionCode == 'buy' :
            direction = '1'     # sell
        elif position.directionCode  == 'sell':
            direction = '0'     # buy
        else:
            return UnkownPositionDirection

        # 发送建单请求
        errorId,errorMsg,data = self.orderInsert(
            instrumentID = position.instrumentID,
            orderRef = order.orderRef,
            direction = direction,
            combOffsetFlag = '1',     #平仓
            volumeTotalOriginal = position.volume
        )

        # 返回平仓结果
        if errorId == 0 :
            # 修改头寸状态
            position.state = 'close'
            position.closePrice = data[0].Price
            position.save()
            # 修改订单状态
            order.state = 'finish'
            order.finishTime = datetime.now()
            order.price = data[0].Price
            order.save()
            # 返回成功
            return 0,u'',position
        else:
            # 保存错误信息
            order.state = 'error'
            order.errorID = errorId
            order.errorMsg = errorMsg
            order.finishTime = datetime.now()
            order.save()
            # 返回错误信息
            return errorId,errorMsg,None


    def closeAll(self,instrumentIDList=None,directionCode=None):
        '''
        关闭满足条件的所有头寸
        instrumentIDList 要平仓的品种列表
        directionCode 要平仓的交易方向
        返回格式:
        如果成功返回:[0,[关闭成功的头寸对应的ModelPosition对象],[]]
        如果失败返回:[关闭失败的数量,[关闭成功的头寸对应的ModelPosition对象],[失败的头寸对应的ModelPosition对象]]
        '''
        # 设置查询条件
        querySet = self.getPositionQuerySet()
        querySet = querySet.filter(state='open')
        if instrumentIDList :
            querySet = querySet.filter(instrumentID__in=instrumentIDList)
        if directionCode :
            querySet = querySet.filter(direction=directionCode)

        # 循环调用关闭头寸过程
        failCount = 0
        failList = []
        successList = []
        for position in querySet:
            errorId,errorMsg,data = self.close(position.id)
            if errorId == 0 :
                successList.append(position)
            else:
                failCount += 1
                failList.append(position)

        # 返回处理结果
        return failCount,successList,failList


    def closePositonByVolume(self):
        '''
        指定手数手数关闭头寸(暂不是实现,这个比较有难度)
        '''
        pass


    def getTotalVolume(self,instrumentIDList=None,directionCode=None):
        '''
        获取头寸手数
        '''
        # 设置查询条件
        querySet = self.getPositionQuerySet()
        querySet = querySet.filter(state__in=['open'])
        if instrumentIDList :
            querySet = querySet.filter(instrumentID__in=instrumentIDList)
        if directionCode :
            querySet = querySet.filter(direction=directionCode)

        # 统计头寸手数
        volume = 0
        for position in querySet:
            volume += position.volume

        # 返回结果
        return volume


    def getPositionQuerySet(self,**kwargs):
        '''
        获取头寸数据集
        主要是封装task,strategyExecuter的过滤操作
        '''
        querySet = ModelPosition.objects.all()
        if self.task:
            querySet = querySet.filter(task=self.task)
        if self.strategyExecuter:
            querySet = querySet.filter(strategyExecuter=self.strategyExecuter)
        return querySet


    def getPositionList(self,state=None):
        '''
        查看头寸
        '''
        # 设置查询条件
        querySet = self.getPositionQuerySet()
        if state:
            querySet = querySet.filter(state=state)

        # 按开仓时间排序
        querySet = querySet.order_by('openTime')

        # 转化位列表结构
        return list(querySet)
