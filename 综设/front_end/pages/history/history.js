var historyList = [];
var repository = require('../../utils/repository.js');
var summary = require('../../utils/summary.js');
var recordStartX = 0;
Page(
    {
        data: {
            historyList: historyList
        }
        ,
        onLoad: function (options) {
            // 页面初始化 options为页面跳转所带来的参数
            console.log('onload');
        },
        onShow: function () {
            console.log('onshow');
            var that = this;
            var types = repository.getDefaultTypes();

            repository.getRecords((data) => {
                console.log('record length:', data.length);
                data.sort((a, b) => {
                    if (a.date === b.date) {
                        return 0;
                    }
                    if (a.date > b.date) {
                        return -1;
                    }
                    if (a.date < b.date) {
                        return 1;
                    }
                });
                data.forEach((i) => {
                    var arr = [];
                    var summaryResult = summary.dateDefaultSummary(i);
                    types.forEach((t) => {
                        arr.push(summaryResult[t.name]);
                    });
                    i.summary = arr;
                });
                that.setData({
                    historyList: data
                });
            });
        },
        historyToggle: function (e) {
            var id = e.currentTarget.id;
            for (var i = 0; i < historyList.length; i++) {
                var item = historyList[i];
                if (item.id === id) {
                    item.open = !item.open;
                } else {
                    item.open = false;
                }
            }
            this.setData({
                historyList: historyList
            });
        }
        ,
        recordStart: function (e) {
            recordStartX = e.touches[0].clientX;
            console.log('startX ', recordStartX);
        }
        ,
        recordMove: function (e) {
            var x = e.touches[0].clientX;
            var mX = recordStartX - x;
            console.log('x ', x);
            console.log('mx ', mX);
            var historyList = this.data.historyList;
            var item = historyList[0];
            var records = item.records;
            records[0].offsetX = 18 - mX;
            this.setData({
                historyList: historyList
            });
        }
        ,
        recordEnd: function (e) {

        }

    }
);