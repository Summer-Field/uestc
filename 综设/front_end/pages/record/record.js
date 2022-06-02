var repository = require('../../utils/repository.js');
var util = require('../../utils/util.js');
const app = getApp()
// Register a Page.
Page({
  data: {
    types: [],
    selectedType: {},
    date: '',
    time: '',
    amount: null,
    remark: '',
    amountInvaild: false
  },
  onLoad: function (options) {
    // 页面初始化 options为页面跳转所带来的参数
    console.log('onload');
    var types = repository.getRecordTypes();
    var selectedType;
    for (var i = 0; i < types.length; i++) {
      var type = types[i];
      if (type.checked) {
        selectedType = type;
      }
    }
    this.setData({
      types: types,
      selectedType: selectedType
    });
    console.log(this.data.selectedType['name'])
  },
  onReady: function () {
    // 页面渲染完成
    console.log('onReady');
  },
  onShow: function () {
    // 页面显示
    console.log("onShow");
    var now = new Date();
    var dateString = util.formatTime(now);
    var arr = dateString.split(' ');
    this.setData({
      date: arr[0],
      time: arr[1]
    });
  },
  onHide: function () {
    // 页面隐藏
    console.log('onHide');
  },
  onUnload: function () {
    // 页面关闭
    console.log('onUnload');
  },
  bindAmountInput: function (e) {
    var amount = e.detail.value;
    this.data.amountInvaild = !amount;
    console.log('amountInvaild:', this.data.amountInvaild);
    this.setData({
      amountInvaild: this.data.amountInvaild
    });
  },
  bindDateChange: function (e) {
    var val = e.detail.value;
    this.data.date = val;
    this.setData({
      date: val
    });
  },
  bindTimeChange: function (e) {
    var val = e.detail.value;
    this.data.time = val;
    this.setData({
      time: val
    });
  },
  selectedTypeChange: function (e) {
    console.log('selectedTypeChange');

    var val = e.detail.value;
    var selectedType;
    var types = this.data.types;
    for (var i = 0; i < types.length; i++) {
      var type = types[i];
      if (type.name === val) {
        console.log(`selected type :${type.name}`);
        type.checked = true;
        selectedType = type;
      }
      else {
        type.checked = false;
      }
    }
    this.setData({
      //types: types,
      selectedType: selectedType
    });
  },
  cancleEvent: function (e) {
    // sent data change to view
    wx.navigateBack({
      delta: 1, // 回退前 delta(默认为1) 页面
      success: function (res) {
        ;
      },
      fail: function (res) {
        // fail
      },
      complete: function (res) {
        // complete
      }
    })
  },
  saveEvent: function (e) {
    var data = this.data;
    var amount = data.amount || data.selectedType.default;
    console.log(`type:${data.selectedType.name} amount:${amount} date:${data.date} time:${data.time} remark:${data.remark}`);
  },
  formSubmit: function (e) {
    var val = e.detail.value;
    var amount = val.amount;

    this.data.amountInvaild = !amount;

    if (this.data.amountInvaild) {
      this.setData({
        amountInvaild: this.data.amountInvaild
      });
      return;
    }
    var date = val.date;
    var time = val.time;
    var type = val.type;
    var remark = val.remark;

    this.data.amount = amount;
    this.data.date = date;
    this.data.time = time;
    this.data.remark = remark;

    console.log(`type:${type} amount:${amount} date:${date} time:${time} remark:${remark}`);
    if (type == '进程数'){
      console.log('here');
      app.globalData.process_num = amount;
      console.log(app.globalData.process_num);
    }else{
      console.log('here2');
      app.globalData.thread_num = amount;
    }
    var record = {
      type: type,
      amount: amount,
      date: date,
      time: time,
      remark: remark,
      unit: this.data.selectedType.unit
    };
    repository.insertRecord(record, (result) => {
      if (result.success) {
        console.log('insertRecord success');
        wx.showToast({
          title: '成功',
          icon: 'success',
          duration: 500
        });
        setTimeout(() => {
          wx.navigateBack({
            delta: 1
          });
        }, 500);
      }
      else {
        console.log('insertRecord fail');
      }
    });
  }
})