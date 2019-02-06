
from django.http.response import HttpResponse
from bson import json_util
from django.views.decorators.csrf import csrf_exempt
import csv
from datetime import datetime, timedelta

ProductReferenceFile = "./ProductDetails/ProductReference.csv"
TransactionInfoFile = "./TransactionInfo/transaction_20190207.csv"

@csrf_exempt
def getTransaction(request,id):
    """
    Fetch the transaction data w.r.t. ID
    :param request:Http Request
    :param id: transaction number
    :return: Transaction information
    """
    if request.method == 'GET':
        if id:
            TransactionInfo = readCSV(TransactionInfoFile)
            for transaction in TransactionInfo:
                # print(transaction)
                # print(id)
                if transaction[0]==id:
                    responseData={ 'transactionId': transaction[0],
                                   'productName': transaction[1],
                                   'transactionAmount': transaction[2],
                                   'transactionDatetime': transaction[3]}
                    return response(responseData)
            return response({'msg': "No ID found", "id": id})
        else:
            return response({"Invalid Request method " + request.method})
    else:
        return response({"No Argument provided"})

@csrf_exempt
def getTransactionSummaryByProducts(request,days):
    """
    Get transaction summary w.r.t Product in the given days
    :param request: Http Request
    :param days: Duration
    :return:Transaction summary
    """
    if request.method == 'GET':
        if days:
            startDate,endDate=calculateDateRange(days)

            ProductReference=readCSV(ProductReferenceFile)
            #print(ProductReference)
            TransactionInfo = readCSV(TransactionInfoFile)
            #print(TransactionInfo)
            summary=[]
            ResponseSummaryList=[]
            products=set()
            #Get dates in between range
            for transaction in TransactionInfo[1:]:
                if startDate >= datetime.strptime(transaction[3], ' %Y-%m-%d %H:%M:%S') >= endDate:
                    summary.append(transaction)
                    products.add(transaction[1])

            if products:
                for product in products:
                    transactionAmount=0
                    productName=""
                    print(ProductReference)
                    print(products)
                    for productdetails in ProductReference:
                        if productdetails[0]==product.strip():
                            productName=productdetails[1]
                    if productName!="":
                        for summaryData in summary:
                            if summaryData[1]==product:
                                transactionAmount=transactionAmount+float(summaryData[2])
                        ResponseSummaryItem={'productName': productName, 'totalAmount':transactionAmount}
                        ResponseSummaryList.append(ResponseSummaryItem)
                    else:
                        return response({'Error': "Some product names are missing"})
            else:
                return response({'summary': "No Summary present for the given range"})

            return response({'summary': ResponseSummaryList})
        else:
            return response({"Invalid Request method " + request.method})
    else:
        return response({"No Argument provided"})

@csrf_exempt
def getTransactionSummaryByManufacturingCity(request,days):
    """
    Get transaction summary w.r.t City in the given days
    :param request: Http Request
    :param days: Duration
    :return:Transaction summary
    """
    if request.method == 'GET':
        if days:
            startDate,endDate=calculateDateRange(days)

            ProductReference=readCSV(ProductReferenceFile)
            #print(ProductReference)
            TransactionInfo = readCSV(TransactionInfoFile)
            #print(TransactionInfo)
            summary=[]
            ResponseSummaryList=[]
            products=set()
            #Get dates in between range
            for transaction in TransactionInfo[1:]:
                if startDate >= datetime.strptime(transaction[3], ' %Y-%m-%d %H:%M:%S') >= endDate:
                    summary.append(transaction)
                    products.add(transaction[1])

            if products:
                for product in products:
                    transactionAmount=0
                    cityName=""
                    # print(ProductReference)
                    # print(products)
                    for productdetails in ProductReference:
                        if productdetails[0]==product.strip():
                            cityName=productdetails[2]
                    if cityName!="":
                        for summaryData in summary:
                            if summaryData[1]==product:
                                transactionAmount=transactionAmount+float(summaryData[2])
                        ResponseSummaryItem={'cityName': cityName, 'totalAmount':transactionAmount}

                        ResponseSummaryList.append(ResponseSummaryItem)
                    else:
                        return response({'Error': "Some product names are missing"})
                print(ResponseSummaryList)
                ResponseSummaryList=removeRedundency(ResponseSummaryList)
                print(ResponseSummaryList)
            else:
                return response({'summary': "No Summary present for the given range"})

            return response({'summary': ResponseSummaryList})
        else:
            return response({"Invalid Request method " + request.method})
    else:
        return response({"No Argument provided"})

def response(msg, status_code=200):
    try:
        responseObj = HttpResponse(
            content=json_util.dumps(msg, default=json_util.default, separators=(',', ':')),
            status=status_code, content_type='application/json')
        return responseObj
    except:
        return response("Error in response obj.", 404)

def readCSV(filename):
    # initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)
    return rows

def calculateDateRange(days):

    startDate=datetime.now()
    endDate = datetime.now() - timedelta(days=int(days))
    print("StartDate:" + str(startDate))
    print("EndDate:" + str(endDate))
    return startDate,endDate

def removeRedundency(ResponseSummaryList):
    final_list = []
    temp_list=[]
    for num in ResponseSummaryList:
        #print(num)
        if num['cityName'] not in temp_list:
            print(final_list)
            temp_list.append(num['cityName'])
            final_list.append(num)
        else:
            for listData in final_list:
                if num['cityName']==listData['cityName']:
                    listData['totalAmount']=listData['totalAmount']+num['totalAmount']
    return final_list