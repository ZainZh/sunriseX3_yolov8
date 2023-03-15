/*
* canvas
*/
function Rendercan(obj) {
  var obj = obj || {};
  this.cid = obj.cid || 'canvas';
  this.did = obj.did || 'domid';
  this.canvas = document.getElementById(this.cid);
  this.ctx = this.canvas.getContext('2d');

  this.isbig = true; // Id是否缩放

  this.h = 24; //左上角三角
  this.lnum = 8; //框角度长出

  this.bgimgs = obj.bgimgs || {};

  this.imgs = [];

  this.csize = {
    w: this.canvas.width,
    h: this.canvas.height
  };
  this.size = {
    w: 1920,
    h: 1080
  };


  this.birdx = 1920
  this.birdy = 1080

  this.init();
}

Rendercan.prototype.init = function() {
  var _this = this;
};

Rendercan.prototype.clear = function() {
  var w = this.canvas.width;
  var h = this.canvas.height;
  var ctx = this.ctx;
  ctx.clearRect(0, 0, w, h);
};

Rendercan.prototype.resize = function() {
  var w = this.canvas.width;
  var h = this.canvas.height;
  this.csize = {
    w: w,
    h: h
  }
};

Rendercan.prototype.datas = function() {
  var w = this.canvas.width;
  var h = this.canvas.height;
  var num = 50;
  var maxsize = 0;
  var minw = w - maxsize;
  var maxh = h - maxsize;
  var arr = [];
  var parr = [];

  for (var i = 0; i < num; i++) {
    var idata = g_point_data[randomNum(0, 9)];
    //arr.push(idata.boxes[0].r)
    arr.push(
      datasize([
        randomNum(0, minw),
        randomNum(0, maxh),
        randomNum(0, minw),
        randomNum(0, maxh)
      ])
    );
  }

  for (var i = 0; i < 70; i++) {
    var idata = g_point_data[randomNum(0, 9)];
    parr.push(idata.points[0].seg[0].p);
  }

  var pnum = 0;
  for (var i in parr) {
    for (var j in parr[i]) {
      this.point(parr[i][j].v);
      pnum++;
    }
    //this.line(parr[i])
  }
};

Rendercan.prototype.datas_box = function(arr) {
  for (var i in arr) {
    var obj = {
      data: arr[i]
    };
    obj.color = [0, 0];
    obj.bgcolor = [0, 1];
    if (arr[i][5] == 2) {
      obj.color = [1, 0];
      obj.bgcolor = [1, 1];
    }
    this.box(obj);
  }
};

// 渲染框
Rendercan.prototype.box = function(obj) {
  var data = obj.data;
  var color = obj.color;
  var bgcolor = obj.bgcolor;
  var bgico = obj.bgico;
  var sw = this.csize.w / this.size.w;
  var sh = this.csize.h / this.size.h;
  var ctx = this.ctx;
  // 点连线
  var okdata = [
    [data[0] * sw, data[1] * sh],
    [data[0] * sw, data[3] * sh],
    [data[2] * sw, data[3] * sh],
    [data[2] * sw, data[1] * sh],
    [data[0] * sw, data[1] * sh]
  ];

  var bw = okdata[2][0] - okdata[0][0];
  var bh = okdata[2][1] - okdata[0][1];
  var ratio = 1;

  if (this.isbig && bw <= 106) ratio = bw / 106;

  // if (obj.data[5] != 1) {
  //   bgc = 'rgba(255,255,255,.04)';
  // } else {
  //   bgc = _color[bgcolor[0]][bgcolor[1]];
  // }
  bgc = 'rgba(255,255,255,.04)';

  ctx.beginPath();
  for (var i in okdata) {
    var idata = okdata[i];
    if (i == 0) {
      ctx.moveTo(idata[0], idata[1]);
    } else {
      ctx.lineTo(idata[0], idata[1]);
    }
  }
  ctx.lineWidth = 1;
  ctx.fillStyle = bgc;
  ctx.fill();
  ctx.strokeStyle = _color[color[0]][1];
  ctx.stroke();
  ctx.closePath();

  // if (obj.data[5] != 1) {
  //   this.idtext({
  //     data: [okdata[0][0], okdata[0][1]],
  //     text: obj.data[5],
  //     tcolor: '#fff',
  //     bcolor: _color[bgcolor[0]][0],
  //     bgcolor: _color[bgcolor[0]][2],
  //     ico: obj.ico,
  //     width: bw
  //   });
  // }

  // 头部 id
  this.idtext({
    data: [okdata[0][0], okdata[0][1]],
    text: obj.data[5],
    tcolor: '#fff',
    bcolor: _color[bgcolor[0]][0],
    bgcolor: _color[bgcolor[0]][2],
    ico: obj.ico,
    width: bw
  });

  var h = this.h;
  var lnum = this.lnum;

  // --- useless code ---- 绘制之前 UI 的边界
  // this.boxboder({
  //   //画左上角三角形
  //   bgc: _color[color[0]][color[1]],
  //   color: color,
  //   data: [
  //     [data[0] * sw, data[1] * sh - h * ratio],
  //     [data[0] * sw, data[1] * sh - h * ratio + lnum * ratio],
  //     [data[0] * sw + lnum * ratio, data[1] * sh - h * ratio]
  //   ]
  // });

  // this.boxboder({
  //   bgc: bgc,
  //   color: color,
  //   data: [
  //     [data[0] * sw + lnum, data[3] * sh],
  //     [data[0] * sw, data[3] * sh],
  //     [data[0] * sw, data[3] * sh - lnum]
  //   ]
  // });

  // this.boxboder({
  //   bgc: bgc,
  //   color: color,
  //   data: [
  //     [data[2] * sw - lnum, data[3] * sh],
  //     [data[2] * sw, data[3] * sh],
  //     [data[2] * sw, data[3] * sh - lnum]
  //   ]
  // });

  // this.boxboder({
  //   bgc: bgc,
  //   color: color,
  //   data: [
  //     [data[2] * sw - lnum, data[1] * sh],
  //     [data[2] * sw, data[1] * sh],
  //     [data[2] * sw, data[1] * sh + lnum]
  //   ]
  // });

  //
  if (obj.issize) {
    ctx.drawImage(
      this.bgimgs[bgico],
      0,
      0,
      obj.issize,
      obj.issize,
      okdata[0][0],
      okdata[0][1],
      bw,
      bh
    );
  } else {
    this.drawIco(this.bgimgs[bgico], bw, bh, okdata[0][0], okdata[0][1]);
  }
};

Rendercan.prototype.box_1 = function(data) {
  //var data = [700,500,900,700,0]
  if (data) {
    var sw = this.csize.w / this.size.w;
    var sh = this.csize.h / this.size.h;

    var ctx = this.ctx;
    //框
    ctx.strokeStyle = _color[data[4]][0];
    ctx.strokeRect(
      data[0] * sw,
      data[1] * sh,
      (data[2] - data[0]) * sw,
      (data[3] - data[1]) * sh
    );
    ctx.fillStyle = 'rgba(0,0,0,0)';
    ctx.fillRect(
      data[0] * sw,
      data[1] * sh,
      (data[2] - data[0]) * sw,
      (data[3] - data[1]) * sh
    );
  } else {
    console.log(data);
  }
};

// 框边界
Rendercan.prototype.boxboder = function(obj) {
  var okdata = obj.data,
    bgc = obj.bgc,
    color = obj.color,
    ctx = this.ctx;
  ctx.beginPath();
  for (var i in okdata) {
    var idata = okdata[i];
    if (i == 0) {
      ctx.moveTo(idata[0], idata[1]);
    } else {
      ctx.lineTo(idata[0], idata[1]);
    }
  }
  ctx.lineWidth = 2;
  ctx.fillStyle = bgc;
  ctx.fill();
  ctx.strokeStyle = _color[color[0]][color[1]];
  ctx.stroke();
};

// id 文字 和背景
Rendercan.prototype.idtext = function(obj) {
  var data = obj.data;
  var tcolor = obj.tcolor || '#fff';
  var color = obj.bcolor || '#fff';
  var bgcolor = obj.bgcolor || '#fff';
  var text = obj.text;
  var ico = obj.ico;

  var ctx = this.ctx;
  var okdata = [[data[0], data[1]]];

  var ratio = 1;
  if (this.isbig && obj.width <= 106) ratio = obj.width / 106;

  var h = this.h * ratio;
  var w = 106 * ratio;
  var s = w - this.h * ratio;

  okdata.push([data[0], data[1] - h]);
  okdata.push([data[0] + s, data[1] - h]);
  okdata.push([data[0] + w, data[1]]);

  ctx.beginPath();
  for (var i in okdata) {
    var idata = okdata[i];
    if (i == 0) {
      ctx.moveTo(idata[0], idata[1]);
    } else {
      ctx.lineTo(idata[0], idata[1]);
    }
  }
  ctx.lineWidth = 1;
  ctx.fillStyle = bgcolor;
  ctx.fill();
  ctx.strokeStyle = color;
  ctx.stroke();

  ctx.beginPath();
  var fontstring = parseInt(14 * ratio) + 'px Arial';
  ctx.font = fontstring;
  ctx.fillStyle = tcolor;
  ctx.textAlign = 'left';
  ctx.fillText(text, data[0] + 28 * ratio, data[1] - 7 * ratio);

  // 画 icon
  // this.drawIco(
  //   this.bgimgs[ico],
  //   15 * ratio,
  //   15 * ratio,
  //   data[0] + 8 * ratio,
  //   data[1] - 20 * ratio
  // );
};

Rendercan.prototype.text = function(obj) {
  var data = obj.data,
    color = obj.color,
    text = obj.text || '888';

  var ctx = this.ctx;
  ctx.font = '16px Arial';
  ctx.fillStyle = _color[color[0]][color[1]];
  ctx.textAlign = 'left';
  ctx.fillText(text, data[0], data[1] - 6);
};

// 渲染单个点
Rendercan.prototype.point = function(obj) {
  var obj = obj || {},
    dara = obj.data,
    color = obj.color || [2, 0],
    r = obj.r || 2;

  var ctx = this.ctx;
  ctx.strokeStyle = _color[color[0]][color[1]];
  ctx.strokeRect(dara[0], dara[1], r, r);
};
// 渲染线
Rendercan.prototype.line = function(obj) {
  var data = obj.data;
  var color = obj.color || 'red';
  var ctx = this.ctx;
  ctx.beginPath();
  for (var i in data) {
    var idata = data[i].v || data[i];
    if (i == 0) {
      ctx.moveTo(idata[0], idata[1]);
    } else {
      ctx.lineTo(idata[0], idata[1]);
    }
  }
  ctx.lineWidth = 1;
  ctx.fillStyle = 'rgba(2,100,30,.2)';
  ctx.fill();
  ctx.strokeStyle = _color[color[0]][color[1]];
  ctx.stroke();
};

Rendercan.prototype.groups = function(data) {
  var data = [
    [640, 280],
    [680, 320],

    [720, 320],
    [740, 200],
    [720, 120],

    [640, 360],
    [540, 360],
    [440, 360],

    [720, 440],

    [660, 500],
    [520, 540],
    [360, 560],

    [760, 520],
    [840, 580],
    [720, 580]
  ];
  var arr = [
    [data[1], data[0]],

    [data[2], data[3]],
    [data[3], data[4]],

    [data[5], data[6]],
    [data[6], data[7]],

    [data[8], data[1]],

    [icenter(data[9], data[12]), data[8]],

    [data[9], data[10]],
    [data[10], data[11]],

    [data[12], data[13]],
    [data[13], data[14]]
  ];
  var robj = {
    0: 16,
    0: 6,
    0: 8,
    0: 10
  };
  for (var i in arr) {
    var obj = {
      data: arr[i]
    };
    this.group(obj);
  }

  function icenter(arr1, arr2) {
    var x = (arr2[0] - arr1[0]) / 2;
    var y = (arr2[1] - arr1[1]) / 2;
    return [arr1[0] + x, arr1[1] + y];
  }
};

// 骨骼连线
Rendercan.prototype.group = function(obj) {
  var xy = obj.data;
  var sw = this.csize.w / this.size.w;
  var sh = this.csize.h / this.size.h;

  var a = xy[1][1] - xy[0][1],
    b = xy[1][0] - xy[0][0],
    c = Math.sqrt(a * a + b * b),
    w = 10,
    h = 14 / 2;

  (ex = xy[0][0] + (b * w) / c),
    (ey = xy[0][1] + (a * w) / c),
    (xw = (b * h) / c),
    (yw = (a * h) / c);

  var x1 = ex - yw;
  var y1 = ey + xw;
  var x2 = ex + yw;
  var y2 = ey - xw;

  var okarr = [xy[0], [x1, y1], xy[1], [x2, y2]];
  var obj = obj || {};
  var data = okarr;
  var color = obj.color || 'red';
  var bgcolor = [5, 0] || 'red';
  var ctx = this.ctx;

  ctx.beginPath();
  for (var i in data) {
    var idata = data[i];
    if (i == 0) {
      ctx.moveTo(idata[0] * sw, idata[1] * sh);
    } else {
      ctx.lineTo(idata[0] * sw, idata[1] * sh);
    }
  }

  //ctx.lineTo(data[0][0],data[0][1]);
  ctx.lineWidth = 1;
  ctx.fillStyle = _color[bgcolor[0]][bgcolor[1]];
  ctx.fill();

  this.can_arc({
    x: data[0][0] * sw,
    y: data[0][1] * sh,
    r: 10
  });
};

Rendercan.prototype.can_arc = function(circle) {
  var color = [6, 0];
  var ctx = this.ctx;
  ctx.beginPath();
  ctx.strokeStyle = _color[color[0]][color[1]];
  // var circle = {
  //     x : 100,    //圆心的x轴坐标值
  //     y : 100,    //圆心的y轴坐标值
  //     r : 10      //圆的半径
  // };
  //沿着坐标点(100,100)为圆心、半径为50px的圆的顺时针方向绘制弧线
  ctx.arc(circle.x, circle.y, circle.r, 0, Math.PI * 2, false);
  //按照指定的路径绘制弧线
  ctx.stroke();
};

// 车道线参考标尺
Rendercan.prototype.can_rule = function(data) {
  var w = this.size.w;
  var sw = this.csize.w / this.size.w;
  var sh = this.csize.h / this.size.h;
  var arr = [];
  for (var i in data) {
    arr.push([[-5 * sw, data[i][0] * sh], [w * sw + 5, data[i][0] * sh]]);
    this.text({
      data: [w * sw - 36, data[i][0] * sh + 0.5],
      color: [2, 0],
      text: data[i][1]
    });
  }
  for (var i in arr) {
    this.line({
      color: [2, 0],
      data: arr[i]
    });
  }
};

Rendercan.prototype.toimg = function(cid, data) {
  var canvas = this.canvas;
  var image = new Image();
  var src = canvas.toDataURL('image/png');
  image.onload = function() {
    var can = document.getElementById(cid);
    can.setAttribute('width', data[2]);
    can.setAttribute('height', data[3]);

    can.getContext('2d').drawImage(image, 0, 0);
    var isrc = can.toDataURL('image/png');
    $('#img_domid2').html(
      '<img style="background: #09f;" src="' + isrc + '"/>'
    );
  };
  image.src = src;
};

Rendercan.prototype.toimgs = function(obj, call) {
  var canvas = this.canvas;
  var image = new Image();
  var src = obj.url;
  var data = obj.data;
  var imgarr = [];
  image.onload = function() {
    for (var i = 2; i < data.length; i++) {
      var can = document.getElementById('canvas_jt'),
        w = data[i][4] - data[i][2];
      h = data[i][5] - data[i][3];
      can.setAttribute('width', w);
      can.setAttribute('height', h);
      can
        .getContext('2d')
        .drawImage(image, data[i][2], data[i][3], w, h, 0, 0, w, h);
      var isrc = can.toDataURL('image/png');
      imgarr.push({
        url: isrc,
        data: data[i]
      });
    }
    call(imgarr);
  };
  image.src = 'data:image/jpeg;base64,' + src;
  //image.src = src
};

Rendercan.prototype.tosimgs = function(obj, call) {
  var image = obj.image;
  var data = obj.data;
  var imgarr = [];
  for (var i = 0; i < data.length; i++) {
    var can = document.getElementById('canvas_jt'),
      w = data[i][2] - data[i][0];
    h = data[i][3] - data[i][1];

    can.setAttribute('width', w);
    can.setAttribute('height', h);
    can
      .getContext('2d')
      .drawImage(image, data[i][0], data[i][1], w, h, 0, 0, w, h);
    var isrc = can.toDataURL('image/png');
    imgarr.push({
      url: isrc,
      data: data[i]
    });
  }
  call(imgarr);
};

Rendercan.prototype.buftoimgs = function(obj, call) {
  var canvas = this.canvas;
  var image = new Image();
  var src = obj.url;
  var data = obj.data;
  var imgarr = [];
  if (!data) return false;
  image.onload = function() {
    for (var i = 0; i < data.length; i++) {
      var can = document.getElementById('canvas_jt'),
        box = data[i]['box'],
        w = box['right'] - box['left'],
        h = box['bottom'] - box['top'];

      var w13 = w * 1.3;
      var h13 = h * 1.3;

      can.setAttribute('width', w13);
      can.setAttribute('height', h13);
      can
        .getContext('2d')
        .drawImage(
          image,
          box['left'] - w * 0.15,
          box['top'] - h * 0.15,
          w13,
          h13,
          0,
          0,
          w13,
          h13
        );
      var isrc = can.toDataURL('image/png');
      imgarr.push({
        url: isrc,
        data: data[i]
      });
    }
    call(imgarr);
  };
  if (src.indexOf('.png') == 0 || src.indexOf('.jpg') == 0) {
    image.src = 'data:image/jpeg;base64,' + src;
  } else {
    image.src = src;
  }
};

Rendercan.prototype.tocanvas = function(cid, data) {
  var image = this.toimg();
  var can = document.getElementById(cid);
  can.setAttribute('width', data[2]);
  can.setAttribute('height', data[3]);

  $('#img_domid2').html(image);

  can.getContext('2d').drawImage(image, 0, 0);
  var src = canvas.toDataURL('image/png');
  //$('#img_domid2').html('<img style="background: #09f;" src="'+src+'"/>')
  return src;
};

Rendercan.prototype.drawImage = function(img) {
  var ctx = this.ctx;
  var csize = this.csize;
  ctx.drawImage(img, 0, 0, csize.w, csize.h);
};

Rendercan.prototype.drawIco = function(img, swidth, sheight, x, y) {
  var ctx = this.ctx;
  ctx.drawImage(img, x, y, swidth, sheight);
};

Rendercan.prototype.addbottombox = function(dom, src, id) {
  var html = '';
  html += '<li class="bottomli">';
  html += '    <img src=' + src + ' class="liimg"/>';
  html += '    <p class="pclass">ID:' + id + '</p>';
  html += '</li>';
  dom.innerHTML += html;
};

Rendercan.prototype.printcanvas = function(cid, pid, data) {
  //新的截图,给坐标截图
  var w = data['x2'] - data['x1'];
  var h = data['y2'] - data['y1'];
  var pic = document.getElementById(pid);
  var canvas_jt = document.getElementById(cid);
  canvas_jt.setAttribute('width', w);
  canvas_jt.setAttribute('height', h);
  canvas_jt
    .getContext('2d')
    .drawImage(pic, data['x1'], data['y1'], w, h, 0, 0, w, h);
  var src = canvas_jt.toDataURL('image/png');
  return src;
};

// 渲染单个点
Rendercan.prototype.testpoint = function(data) {
  /*
    var data = [
                {x: 1525, y: 123, score: 1},
                {x: 1532, y: 111, score: 1},
                {x: 1502, y: 116, score: 1},
                {x: 1566, y: 107, score: 1},
                {x: 1534, y: 117, score: 1},
                {x: 1545, y: 126, score: 1},
                {x: 1396, y: 136, score: 1},
                {x: 1537, y: 181, score: 1},
                {x: 1537, y: 188, score: 1},
                {x: 1541, y: 174, score: 1},
                {x: 1490, y: 172, score: 1},
                {x: 1532, y: 334, score: 1},
                {x: 1482, y: 326, score: 1},
                {x: 1533, y: 392, score: 1},
                {x: 1526, y: 387, score: 1},
                {x: 1594, y: 593, score: 1},
                {x: 1452, y: 603, score: 1}
            ]
    */

  var color = [1, 0],
    r = 3;

  var sw = this.csize.w / this.size.w;
  var sh = this.csize.h / this.size.h;

  var ctx = this.ctx;

  for (var i in data) {
    ctx.lineJoin = 'bevel';
    ctx.strokeStyle = _color[color[0]][color[1]];
    ctx.strokeRect(data[i].x * sw, data[i].y * sh, r, r);

    ctx.fillStyle = _color[color[0]][color[1]];
    ctx.fillRect(data[i].x * sw, data[i].y * sh, r, r);
    //ctx.fillText(i, data[i].x, data[i].y-6);
  }
};

//html 渲染
Rendercan.prototype.htmlbox = function(data) {
  var sw = 500 / 1920;
  var sh = 500 / 1080;
  var html =
    '<div style="position: absolute; left: ' +
    data[0] * sw +
    'px; right: ' +
    data[1] * sw +
    'px; width: ' +
    (data[2] - data[0]) * sw +
    'px; height: ' +
    (data[3] - data[1]) * sh +
    'px;border: 1px solid #f00"></div>';
  return html;
};

//html 渲染
Rendercan.prototype.htmlpoint = function(data) {
  var size = 2;
  var sw = 500 / 1920;
  var sh = 500 / 1080;
  var html =
    '<div style="position: absolute; left: ' +
    data[0] * sw +
    'px; right: ' +
    data[1] * sw +
    'px; width: ' +
    size +
    'px; height: ' +
    size +
    'px;border: 1px solid #f00; border-radius: 10px;"></div>';
  return html;
};

Rendercan.prototype.drawmask = function() {
  var ctx = this.ctx;
  ctx.beginPath;
  ctx.fillStyle = 'rgba(28, 29, 59,0.5)';
  ctx.fillRect(0, 0, this.csize.w, this.csize.h);
  ctx.closePath();
};

// 轨迹绘制
Rendercan.prototype.drawpath = function(arr, color) {
  var sw = this.csize.w / this.birdx;
  var sh = this.csize.h / this.birdy;
  var ctx = this.ctx;
  ctx.beginPath();
  arr.forEach(point, index => {
    var x = point.x * sw
    var y = point.y * sh
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y)
    }
  })
  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  ctx.stroke();
};

function datasize(data) {
  var arr = [data[0], data[1], data[2], data[3]];
  if (data[0] > data[2]) {
    arr[0] = data[2];
    arr[2] = data[0];
  }
  if (data[1] > data[3]) {
    arr[1] = data[3];
    arr[3] = data[1];
  }
  return arr;
}

var _color = [
  ['rgba(206,0,84,1)', 'rgba(206,0,84,.3)', 'rgba(206,0,84,.6)'], // 红色  女人
  ['rgba(36,185,255,1)', 'rgba(36,185,255,.3)', 'rgba(36,185,255,.6)'], // 蓝色 男人
  ['rgba(17,201,170,1)', 'rgba(17,201,170,.3)', 'rgba(17,201,170,.6)'], // 绿色 车
  ['rgba(255,232,135,1)', 'rgba(255,232,135,.3)', 'rgba(255,232,135,.6)'], // 车
  ['rgba(247,128,36,1)', 'rgba(247,128,36 ,.3)', 'rgba(247,128,36 ,.6)'], // 行人
  ['rgba(0,188,246,1)', 'rgba(0,188,246  ,.3)', 'rgba(0,188,246  ,.6)'], // 车道线
  ['rgba(255,255,255,1)', 'rgba(255,255,255,.3)', 'rgba(255,255,255,.6)'], // 文字颜色白色
  ['rgba(255,255,255,1)', 'rgba(255,255,255,.3)', 'rgba(255,255,255,.6)'], // 文字颜色白色
  ['rgba(37,211,255,1)', 'rgba(37,211,255,.3)', 'rgba(37,211,255,.6)'], // 骨骼点
  ['rgba(255,217,37,1)', 'rgba(255,217,37,.3)', 'rgba(255,217,37,.6)'] // 骨骼圆
];
