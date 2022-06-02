var detailList = [];
var repository = require('../../utils/repository.js');
var recordStartX = 0;
var currentOffsetX = 0;
Page(
    {
        data: {
            detailList: detailList,
            date:''
        }
        ,
        onLoad: function (op) {
            var that = this;
            var date = op.date;
            that.data.date = date;
            wx.setNavigationBarTitle({
                title: date,
                success: function (res) {
                    // success
                }
            });
            repository.findDateNode(date, (result) => {
                if (result.success) {
                    that.data.detailList = result.result.records;
                    that.setData({
                        detailList: result.result.records
                    });
                }
            });
        }
        ,
        recordStart: function (e) {
            var index = e.currentTarget.dataset.index;
            console.log(e.target.dataset);
            console.log(e.currentTarget.dataset);

            console.log(index);
            if (index === undefined) {
                return;
            }

            recordStartX = e.touches[0].clientX;
            var item = this.data.detailList[index];
            if (item['offsetX'] === undefined) {
                item.offsetX = 0;
            }
            currentOffsetX = item.offsetX;
            console.log('start x ', recordStartX);
        }
        ,
        recordMove: function (e) {
            var index = e.currentTarget.dataset.index;
            console.log(index);
            if (index === undefined) {
                return;
            }

            var detailList = this.data.detailList;
            var item = detailList[index];
            var x = e.touches[0].clientX;
            var mx = recordStartX - x;
            console.log('move x ', mx);

            var result = currentOffsetX - mx;
            if (result >= -80 && result <= 0) {
                item.offsetX = result;
            }
            this.setData({
                detailList: detailList
            });
        }
        ,
        recordEnd: function (e) {
            var index = e.currentTarget.dataset.index;
            console.log(index);
            if (index === undefined) {
                return;
            }

            var detailList = this.data.detailList;
            var item = detailList[index];
            console.log('end x ', item.offsetX);

            if (item.offsetX < -40) {
                item.offsetX = -80;

            } else {
                item.offsetX = 0;

            }
            this.setData({
                detailList: detailList
            });
        },
        deleteRecordEvent: function (e) {
            var that = this;
            var index = e.currentTarget.dataset.index;
            console.log(index);
            if (index === undefined) {
                return;
            }
            repository.findDateNode(this.data.date, (result) => {
                if (result.success) {
                    var detailList = result.result.records;
                    detailList.splice(index, 1);
                    that.setData({
                        detailList: detailList
                    });
                    repository.saveRecords((r) => {
                        console.log(r);
                    });
                }
            });

        }

    }
);