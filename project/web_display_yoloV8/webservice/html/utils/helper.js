const ATTRIBUTES = {
  type: {
    '0': '大货车', 
    '1': '公交车', 
    '2': '小货车', 
    '3': '商务车', 
    '4': '面包车', 
    '5': '中巴车', 
    '6': '越野车', 
    '7': '代步车', 
    '8': '轿车', 
    '9': '专用作业车', 
    '10': '三轮车', 
    '11': '其他'
  },
  color: {
    '0': '白', 
    '1': '银灰', 
    '2': '黑', 
    '3': '红', 
    '4': '棕', 
    '5': '蓝', 
    '6': '黄', 
    '7': '紫', 
    '8': '绿', 
    '9': '粉', 
    '10': '青', 
    '11': '金', 
    '12': '其他'
  },
  gender: {
    '1': '男',
    '-1': '女'
  }
}

function getAttributesValue(obj) {
  let type = ATTRIBUTES[obj.type]
  let value = ''
  Object.keys(type).map(function(key) {
    if(String(obj.value) === key) {
      value = type[key]
    }
  })
  return { type: obj.type, value }
}

function getURLParameter(name) {
  var location = self.location
  return (
    decodeURIComponent(
      (new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(
        location.search
      ) || [null, ''])[1].replace(/\+/g, '%20')
    ) || null
  );
}

function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint16Array(buf));
}

// 获取 url query 参数
function getUrlQueryParameter(name) {
  var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
  var r = window.location.search.substr(1).match(reg);
  if (r != null) return decodeURI(r[2]);
  return null;
}

// 时间戳转常规时间
function toNormalTime(timestamp) {
  var date = new Date(timestamp);
  var hour = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();

  hour = hour >= 10 ? hour : `0${hour}`;
  minutes = minutes >= 10 ? minutes : `0${minutes}`;
  seconds = seconds >= 10 ? seconds : `0${seconds}`;

  return `${hour}:${minutes}:${seconds}`;
}

function toNormalTimeComplete(timestamp) {
  var time = new Date(timestamp);
  var year = time.getFullYear();
  var month = time.getMonth() + 1;
  var date = time.getDate();
  var hour = time.getHours();
  var minutes = time.getMinutes();
  var seconds = time.getSeconds();

  hour = hour >= 10 ? hour : `0${hour}`;
  minutes = minutes >= 10 ? minutes : `0${minutes}`;
  seconds = seconds >= 10 ? seconds : `0${seconds}`;
  month = month >= 10 ? month : `0${month}`;
  date = date >= 10 ? date : `0${date}`;


  return `${year}-${month}-${date}  ${hour}:${minutes}:${seconds}`;
}

var timestamp = new Date().valueOf();
function printInterval() {
  var current = new Date().valueOf();
  var interval = current - timestamp;
  if (interval > 0) {
    console.info(interval);
  }
  timestamp = current;
}


function getGender(sex) {
  var gender;
  switch(sex) {
    case 0:
      gender = '女性';
      break;
    case 1:
      gender = '男性';
      break;
    case -1:
      gender = '未识别';
      break;
    default:
      null;
  }
  return gender;
}

function getGeneration(age) {
  var generation;

  if (age <= 2) {
    generation = '幼年';
  } else if(age <= 4){
    generation = '青年';
  } else if(age <= 6){
    generation = '中年';
  } else {
    generation = '老年'
  }

  return generation;
}

// 去除相邻元素
Array.prototype.distinctCloseTo = function() {  
  var $ = this;  
  var o3 = new Array();  
  var t = 0  
  for (var i = 0; i < $.length; i++) {  
    if ($[i] != $[i - 1]) {  
      o3[t] = $[i];  
      t++;  
    }  
  }  
  $.length = 0;  
  for (var j = 0; j < o3.length; j++) {  
    $[j] = o3[j];  
  }  
  return o3;  
} 

// 分割数组
function sliceArray(array, size) {
  var result = [];
  for (var x = 0; x < Math.ceil(array.length / size); x++) {
    var start = x * size;
    var end = start + size;
    result.push(array.slice(start, end));
  }
  return result;
}


