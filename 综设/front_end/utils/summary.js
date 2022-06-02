var repository = require('../utils/repository.js');
var util = require('../utils/util.js');

var sevenDaySummary = function () {
    var dates = [];
    var types = repository.getRecordTypes();
    var todayVal = new Date().valueOf();
    for (var i = 0; i < 7; i++) {
        var today = new Date(todayVal);
        var date = today.getDate();

        today.setDate(date - i);
        dates.push(today);
    }
    var result = {};
    dates.forEach((d) => {
        var dateStr = util.formatDate(d);
        repository.findDateNode(dateStr, (r) => {
            if (r.success) {
                var node = r.result;
                var summary = dateSummary(node,types);
                result[dateStr] = summary;
            }
            else {
                result[dateStr] = {};
            }
        });
    });
    return result;
}
var dateSummary = function (dateNode, types) {
    var result = {};
    types.forEach((i) => {
        result[i.name] = {
            name: i.name,
            unit: i.unit,
            totalAmount: 0
        };
    });
    if (dateNode.records) {
        for (var i = 0; i < dateNode.records.length; i++) {
            var record = dateNode.records[i];
            var amount = parseInt(record.amount);
            var typeResult = result[record.type];
            if (!typeResult) {
                typeResult = {
                    name: record.type,
                    unit: record.unit,
                    totalAmount: amount
                };
            }
            else {
                typeResult.totalAmount += amount;
            }
        }
    }

    return result;
}
var dateDefaultSummary = function (dateNode) {
    var types = repository.getDefaultTypes();
    return dateSummary(dateNode, types);
}

module.exports.sevenDaySummary = sevenDaySummary;
module.exports.dateDefaultSummary = dateDefaultSummary;