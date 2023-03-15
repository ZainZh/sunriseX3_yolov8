function Renderske(obj) {
  var obj = obj || {};
  this.cid = obj.cid || 'canvas';
  this.canvas = document.getElementById(this.cid);
  this.ctx = this.canvas.getContext('2d');
  this.colortype = {
    pink: ['rgb(179, 75, 234)', 'rgb(240, 119, 192)', 'rgb(111, 32, 255)'],
    blue: ['rgb(68, 246, 230)', 'rgb(67, 190, 225)', 'rgb(23, 100, 255)'],
    orange: ['rgb(255, 174, 0', 'rgb(235,91,1)', 'rgb(235,91,1)']
  };
  this.canvas.width = obj.width || 1920;
  this.canvas.height = obj.height || 1080;

  // this.csize = {
  //   w: this.canvas.width,
  //   h: this.canvas.height
  // };

  this.width = 8;
  this.shortlength = 8;
}


// drawRect
// drawLine
// drawCircle
// drawOuntline


Renderske.prototype.drawImage = function(img) {
  var ctx = this.ctx;
  ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
};

Renderske.prototype.clear = function() {
  var w = this.canvas.width;
  var h = this.canvas.height;
  var ctx = this.ctx;
  ctx.clearRect(0, 0, w, h);
};

Renderske.prototype.drawcircle = function(point, r, color) {
  var x1 = point[0];
  var y1 = point[1];
  var ctx = this.ctx;
  ctx.beginPath();
  var linearGradient1 = ctx.createLinearGradient(x1, y1 - r, x1, y1 + r);
  linearGradient1.addColorStop(0, this.colortype[color][0]);
  linearGradient1.addColorStop(1, this.colortype[color][1]);
  // ctx.StrokeStyle = 'rgb(240, 119, 192)';

  ctx.lineWidth = 4;
  ctx.strokeStyle = linearGradient1;
  // ctx.arc(x1,y1,r,0,2*Math.PI);
  EllipseOne(ctx, x1, y1, r - 2, 1.5 * r);
  ctx.closePath();

  function EllipseOne(context, x, y, a, b) {
    var step = a > b ? 1 / a : 1 / b;
    context.beginPath();
    context.moveTo(x + a, y);
    for (var i = 0; i < 2 * Math.PI; i += step) {
      context.lineTo(x + a * Math.cos(i), y + b * Math.sin(i));
    }
    context.closePath();
    ctx.stroke();
  }
};

Renderske.prototype.drawrect = function(p1, p2, p3, p4, color) {
  var x1 = p1[0];
  var y1 = p1[1];
  var x2 = p2[0];
  var y2 = p2[1];
  var x3 = p3[0];
  var y3 = p3[1];
  var x4 = p4[0];
  var y4 = p4[1];

  var ctx = this.ctx;
  ctx.beginPath();
  var linearGradient1 = ctx.createLinearGradient(x1, y1, x3, y3);
  linearGradient1.addColorStop(0, this.colortype[color][0]);
  linearGradient1.addColorStop(1, this.colortype[color][1]);
  // ctx.StrokeStyle = 'rgb(240, 119, 192)';
  ctx.lineCap = 'round';
  ctx.lineWidth = this.width;
  ctx.strokeStyle = linearGradient1;
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.lineTo(x3, y3);
  ctx.lineTo(x4, y4);
  ctx.lineTo(x1, y1);
  ctx.stroke();
  ctx.closePath();
};

//参数分别是点1 点2  缩短方式（两边都缩短both 缩短一边是one 不缩短是nones） 颜色

Renderske.prototype.drawline = function(point1, point2, side, color) {
  var points = this.shorter(point1, point2);
  var p1, p2;
  if (side == 'both') {
    p1 = points[0];
    p2 = points[1];
  } else if (side == 'one') {
    p1 = points[0];
    p2 = point2;
  } else {
    p1 = point1;
    p2 = point2;
  }
  var x1 = p1[0];
  var y1 = p1[1];
  var x2 = p2[0];
  var y2 = p2[1];
  var ctx = this.ctx;
  ctx.beginPath();
  var linearGradient1 = ctx.createLinearGradient(x1, y1, x2, y2);
  linearGradient1.addColorStop(0, this.colortype[color][0]);
  linearGradient1.addColorStop(1, this.colortype[color][1]);
  // ctx.StrokeStyle = 'rgb(240, 119, 192)';
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.lineWidth = this.width;
  ctx.lineCap = 'butt';
  ctx.strokeStyle = linearGradient1;
  ctx.stroke();
  ctx.closePath();
  this.drawend(p1, p2, this.colortype[color][2]);
};

Renderske.prototype.shorter = function(p1, p2) {
  var x1 = p1[0];
  var y1 = p1[1];
  var x2 = p2[0];
  var y2 = p2[1];
  var x = Math.abs(x2 - x1);
  var y = Math.abs(y2 - y1);
  var z = Math.sqrt(x * x + y * y);
  var detax1 = x1;
  var detax2 = x2;
  var detay1 = y1;
  var detay2 = y2;

  if (x2 - x1 != 0) {
    var k = (y2 - y1) / (x2 - x1);
    var b = (-x1 * (y2 - y1)) / (x2 - x1) + y1;
    var cos = x / z;
    var deta = this.shortlength * cos;
    detax1 = x1 + deta * (x2 - x1 > 0 ? 1 : -1);
    detax2 = x2 + deta * (x1 - x2 > 0 ? 1 : -1);
    detay1 = k * detax1 + b;
    detay2 = k * detax2 + b;
  } else {
    detay1 = y1 + this.shortlength * (y2 - y1 > 0 ? 1 : -1);
    detay2 = y2 + this.shortlength * (y1 - y2 > 0 ? 1 : -1);
  }
  return [[detax1, detay1], [detax2, detay2]];
};

Renderske.prototype.box = function(obj) {
  this.colortype = obj.color || this.colortype;
  this.width = obj.width || this.width;
  this.shortlength = this.width;
  var p = $.extend(true, [], obj['points']);
  // for (var i in p) {
  //   if (p[i]) {
  //     p[i][0] = p[i][0] * this.ratiow;
  //     p[i][1] = p[i][1] * this.ratioh;
  //   }
  // }
  var t1, t2, b1, b2;

  if (p['left_hip'].slice(0, 2)[0] < p['right_hip'].slice(0, 2)[0]) {
    //判断HIP左右
    b1 = p['left_hip'].slice(0, 2);
    b2 = p['right_hip'].slice(0, 2);
  } else {
    b1 = p['right_hip'].slice(0, 2);
    b2 = p['left_hip'].slice(0, 2);
  }

  if (p['left_shoulder'].slice(0, 2)[0] < p['right_shoulder'].slice(0, 2)[0]) {
    //判断SHOULDER左右
    t1 = p['left_shoulder'].slice(0, 2);
    t2 = p['right_shoulder'].slice(0, 2);
  } else {
    t1 = p['right_shoulder'].slice(0, 2);
    t2 = p['left_shoulder'].slice(0, 2);
  }
  var temp;
  if (t1[1] > b1[1]) {
    //上下换
    temp = b1;
    b1 = t1;
    t1 = temp;
  }
  if (t2[1] > b2[1]) {
    //上下换
    temp = b2;
    b2 = t2;
    t2 = temp;
  }

  this.drawrect(t1, t2, b2, b1, 'orange');

  var l1 = p['left_ear'][0];
  var l2 = p['left_ear'][1];
  var r1 = p['right_ear'][0];
  var r2 = p['right_ear'][1];
  var midpoint = [(l1 + r1) / 2, (l2 + r2) / 2];
  var r = Math.sqrt((r1 - l1) * (r1 - l1) + (r2 - l2) * (r2 - l2)) / 2;

  this.drawcircle(midpoint, r, 'orange');
  this.drawend(
    p['left_ear'].slice(0, 2),
    p['right_ear'].slice(0, 2),
    'rgb(111, 32, 255)'
  );
  this.drawline(
    p['left_wrist'].slice(0, 2),
    p['left_elbow'].slice(0, 2),
    'none',
    'blue'
  );
  this.drawline(
    p['left_elbow'].slice(0, 2),
    p['left_shoulder'].slice(0, 2),
    'both',
    'blue'
  );

  this.drawline(
    p['right_wrist'].slice(0, 2),
    p['right_elbow'].slice(0, 2),
    'none',
    'pink'
  );
  this.drawline(
    p['right_elbow'].slice(0, 2),
    p['right_shoulder'].slice(0, 2),
    'both',
    'pink'
  );

  this.drawline(
    p['left_hip'].slice(0, 2),
    p['left_knee'].slice(0, 2),
    'both',
    'blue'
  );
  this.drawline(
    p['left_knee'].slice(0, 2),
    p['left_ankle'].slice(0, 2),
    'none',
    'blue'
  );

  this.drawline(
    p['right_hip'].slice(0, 2),
    p['right_knee'].slice(0, 2),
    'both',
    'pink'
  );
  this.drawline(
    p['right_knee'].slice(0, 2),
    p['right_ankle'].slice(0, 2),
    'none',
    'pink'
  );
};

Renderske.prototype.drawend = function(p1, p2, color) {
  var x1 = p1[0];
  var y1 = p1[1];
  var x2 = p2[0];
  var y2 = p2[1];
  var points = this.shorter(p1, p2);
  var ctx = this.ctx;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineCap = 'butt';
  ctx.lineTo(points[0][0], points[0][1]);
  ctx.moveTo(x2, y2);
  ctx.lineTo(points[1][0], points[1][1]);
  ctx.lineWidth = this.width;
  ctx.strokeStyle = color;
  ctx.stroke();
  ctx.closePath();
};


Renderske.prototype.drawBodyBox = function(p1, p2) {
  var x1 = p1[0];
  var y1 = p1[1];
  var x2 = p2[0];
  var y2 = p1[1];
  var x3 = p2[0];
  var y3 = p2[1];
  var x4 = p1[0];
  var y4 = p2[1];

  var ctx = this.ctx;
  ctx.beginPath();
  var linearGradient1 = ctx.createLinearGradient(x1, y1, x3, y3);
  linearGradient1.addColorStop(0, this.colortype['blue'][0]);
  linearGradient1.addColorStop(1, this.colortype['blue'][1]);
  // ctx.StrokeStyle = 'rgb(240, 119, 192)';
  ctx.lineCap = 'round';
  ctx.lineWidth = this.width;
  ctx.strokeStyle = linearGradient1;
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.lineTo(x3, y3);
  ctx.lineTo(x4, y4);
  ctx.lineTo(x1, y1);
  ctx.stroke();
  ctx.closePath();
}


// Useless
// Renderske.prototype.resize = function(obj) {
//   this.csize = {
//     w: obj['cwidth'],
//     h: obj['cheight']
//   };
//   this.canvas.width = this.csize.w;
//   this.canvas.height = this.csize.h;
//   this.ratiow = this.csize.w / (this.size.w || 960);
//   this.ratioh = this.csize.h / (this.size.h || 540);
// };
