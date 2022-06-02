var defaultTypes = [
    { name: '进程数', unit: '个', checked: true },
    { name: '线程数', unit: '个' },
    // { name: '开水', unit: 'ml' },
    // { name: '便便', unit: '次', default: 1 }
];

var global_records;

var reset = function (callback) {
    wx.clearStorage({
        success: function (res) {
            global_records = [];
            callback({
                success: true
            });
        },
        fail: function (res) {
            callback({
                success: false
            });
        },
        complete: function (res) {
            // complete
        }
    })
}

var getRecords = function (callback) {
    if (callback) {
        if (global_records) {
            callback(global_records);
        }
        else {
            wx.getStorage({
                key: 'records',
                success: function (res) {
                    // success
                    global_records = res.data;
                    callback(global_records);
                },
                fail: function (res) {
                    // fail
                    console.log('get records from storage fail .');
                    wx.setStorage({
                        key: 'records',
                        data: []
                    });
                    global_records = [];
                    callback(global_records);
                },
                complete: function (res) {
                    // complete
                }
            })
        }

    }
};

var findDateNode = function (date, callback) {
    getRecords((records) => {
        for (var i = 0; i < records.length; i++) {
            var node = records[i];
            if (node.date === date) {
                callback({
                    success: true,
                    result: node
                });
                return;
            }
        }

        callback({
            success: false
        });
    });
}

var insertRecord = function (record, callback) {
    findDateNode(record.date, (data) => {
        if (data.success) {
            //find
            var dateNode = data.result;
            dateNode.records.push(record);
            dateNode.records.sort((a, b) => {
                if (a.time === b.time) {
                    return 0;
                }
                if (a.time > b.time) {
                    return 1;
                }
                if (a.time < b.time) {
                    return -1;
                }
            });

            saveRecords(callback);
        } else {
            //not find
            var dateNode = {
                date: record.date,
                records: []
            };
            dateNode.records.push(record);
            getRecords((records) => {
                records.unshift(dateNode);
                saveRecords(callback);
            });
        }
    });
}

var deleteRecord = function (recordId, callback) {

}

var saveRecords = function (callback) {
    //save records to stornage
    wx.setStorage({
        key: 'records',
        data: global_records,
        success: function () {
            callback({
                success: true
            });
        },
        fail: function () {
            callback({
                success: false
            });
        }
    });
}

var getTypes = function () {
    var customTypes = getCustomTypes();
    var types = [];
    for (var i = 0; i < defaultTypes.length; i++) {
        var item = defaultTypes[i];
        types.push(item);
    }
    for (var i = 0; i < customTypes.length; i++) {
        var item = customTypes[i];
        types.push(item);
    }

    return types;
}

var getDefaultTypes = function () {
    return defaultTypes;
}

var getCustomTypes = function () {
    var customTypes = wx.getStorageSync('recordTypes') || [];
    return customTypes;
}

var insertCustomType = function (t, callback) {
    var customTypes = getCustomTypes();
    var exists = customTypes.find((ct) => {
        return ct.name === t.name;
    });
    if (exists) {
        callback({
            success: true
        });
        return;
    }
    customTypes.push(t);
    wx.setStorage({
        key: 'recordTypes',
        data: customTypes,
        success: () => {
            callback({
                success: true
            });
        },
        fail: () => {
            callback({
                success: false
            });
        }
    });
}

var saveCustomTypes = function (types, callback) {
    wx.setStorage({
        key: 'recordTypes',
        data: types,
        success: () => {
            callback({
                success: true
            });
        },
        fail: () => {
            callback({
                success: false
            });
        }
    });
}

module.exports.getDefaultTypes = getDefaultTypes;
module.exports.getRecordTypes = getTypes;
module.exports.getRecords = getRecords;
module.exports.getCustomTypes = getCustomTypes;
module.exports.insertRecord = insertRecord;
module.exports.findDateNode = findDateNode;
module.exports.saveRecords = saveRecords;
module.exports.insertCustomType = insertCustomType;
module.exports.saveCustomTypes = saveCustomTypes;
module.exports.reset = reset;