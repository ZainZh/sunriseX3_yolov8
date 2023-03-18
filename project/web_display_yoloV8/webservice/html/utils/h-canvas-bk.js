function HCanvas(obj) {
  var obj = obj || {};

  this.canvasId = obj.canvasId || 'canvas';
  this.canvas = obj.canvas || document.getElementById(this.canvasId);
  this.context = this.canvas.getContext('2d');

  // 画布尺寸
  this.canvas.width = obj.width || 1920;
  this.canvas.height = obj.height || 1080;

  this.imgs = obj.imgs || [];
}

HCanvas.prototype.clear = function () {
  this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
};

HCanvas.prototype.drawImage = function (img, x = 0, y = 0, width = this.canvas.width, height = this.canvas.height) {
  var context = this.context;
  context.drawImage(img, x, y, width, height);
};

HCanvas.prototype.drawBorderImage = function ({
                                                img = {},
                                                x = 0,
                                                y = 0,
                                                width = this.canvas.width,
                                                height = this.canvas.height,
                                                id = '',
                                                color = 'rgba(255,255,255,1)',
                                                changed = false,
                                                callback } = {}) {

  if (img.src === '') {
    return;
  }

  var context = this.context;
  // 图片超出边界处理
  let canvas = document.querySelector('#path');
  x = (x + width > canvas.offsetWidth) ? canvas.offsetWidth - width : x;
  y = (y + height > canvas.offsetHeight) ? canvas.offsetHeight - height : y;

  y += 1 / 4 * height;   //整体下移

  //绘制header
  context.beginPath();
  context.moveTo(x, y);
  context.lineTo(x, y - 1 / 4 * height);
  context.lineTo(x + 3 / 4 * width, y - 1 / 4 * height);
  context.lineTo(x + width, y);
  context.closePath();
  context.fillStyle = color;
  context.lineWidth = 1.5;
  context.strokeStyle = color;
  context.fill();
  context.stroke();

  //绘制文本
  context.beginPath();
  var fontstring = 14 + 'px Arial';
  context.font = fontstring;
  context.textAlign = 'left';
  context.fillStyle = 'rgba(255,255,255,1)';
  context.fillText(id, x + 5, y - 5);

  //绘制边框
  context.beginPath();
  context.moveTo(x, y);
  context.lineTo(x + width, y);
  context.lineTo(x + width, y + height);
  context.lineTo(x, y + height);
  context.strokeStyle = color;
  context.lineWidth = 3;
  context.closePath();
  context.stroke();

  if (changed) {
    img.onload = () => {
      context.drawImage(img, x, y, width, height);//绘制人像
      callback(id, false);
    }
  } else {
    context.drawImage(img, x, y, width, height);//绘制人像
  }
};

HCanvas.prototype.drawLine = function (p1, p2, option) {
  var x1 = p1.x;
  var y1 = p1.y;
  var x2 = p2.x;
  var y2 = p2.y;
  option = option || {};

  var context = this.context;
  var lineWidth = option.lineWidth || 4;
  var strokeColor = option.strokeColor || '#0FF';

  context.beginPath();

  context.moveTo(x1, y1);
  context.lineTo(x2, y2);

  context.lineWidth = lineWidth;
  context.strokeStyle = strokeColor;
  context.stroke();
};

HCanvas.prototype.drawPoint = function (x, y, option) {
  var context = this.context;
  var lineWidth = option.lineWidth || 2;
  var radius = option.radius || 5;

  context.lineWidth = lineWidth;
  context.strokeStyle = option.strokeColor || '#0FF';
  context.fillStyle = option.fillColor || 'white';

  context.beginPath();
  context.arc(x, y, radius, 0, Math.PI * 2, true);
  context.closePath();
  context.fill();
  context.stroke();
};

HCanvas.prototype.drawLandMark = function (points) {
  points.map(point => {
    var context = this.context;
    var lineWidth = 1;
    var radius = 2;

    context.lineWidth = lineWidth;
    context.strokeStyle = '#0FF';
    context.fillStyle = 'white';

    context.beginPath();
    context.arc(point.x_, point.y_, radius, 0, Math.PI * 2, true);
    context.closePath();
    context.fill();
    context.stroke();
  });
};

HCanvas.prototype.drawRect = function (p1, p2, option = { lineWidth: 1, strokeColor: 'white', fillColor: 'rgba(255,255,255,0)' }) {
  if (typeof p1.x === 'undefined') {
    return;
  }
  var context = this.context;
  var x = p1.x;
  var y = p1.y;
  var width = p2.x - p1.x;
  var height = p2.y - p1.y;
  var lineWidth = option.lineWidth || 1;
  var strokeColor = option.strokeColor || 'white';
  var fillColor = option.fillColor || 'rgba(255,255,255,0)';
  context.beginPath();
  context.lineWidth = lineWidth;
  context.strokeStyle = strokeColor;
  context.fillStyle = fillColor;
  context.rect(x, y, width, height);
  context.stroke();
  context.fill();
  context.restore();
  context.closePath();
};

HCanvas.prototype.drawCorner = function (
  p1,
  p2,
  { outerOffset = 10, innerOffset = 7, fillStyle = 'rgba(0,204,187,0.8)' } = {}
) {
  var context = this.context;

  context.fillStyle = fillStyle;
  context.beginPath();
  context.moveTo(p1.x + outerOffset, p1.y - outerOffset);
  context.lineTo(p1.x + innerOffset, p1.y - innerOffset);
  context.lineTo(p1.x - innerOffset, p1.y - innerOffset);
  context.lineTo(p1.x - innerOffset, p1.y + innerOffset);
  context.lineTo(p1.x - outerOffset, p1.y + outerOffset);
  context.lineTo(p1.x - outerOffset, p1.y - outerOffset);
  context.closePath();
  context.fill();

  context.beginPath();
  context.moveTo(p2.x - outerOffset, p2.y + outerOffset);
  context.lineTo(p2.x - innerOffset, p2.y + innerOffset);
  context.lineTo(p2.x + innerOffset, p2.y + innerOffset);
  context.lineTo(p2.x + innerOffset, p2.y - innerOffset);
  context.lineTo(p2.x + outerOffset, p2.y - outerOffset);
  context.lineTo(p2.x + outerOffset, p2.y + outerOffset);
  context.closePath();
  context.fill();
};


HCanvas.prototype.drawBodyBox = function (p1, p2) {
  var lineWidth = 2;
  var strokeColor = '#00CCBB';
  var fillColor = 'rgba(0,204,187,0.3)'
  var width = p2.x - p1.x;
  var height = p2.y - p1.y;
  var offset = Math.min(width / 12, height / 12);
  var outerOffset, innerOffset;

  if (offset > 15) {
    outerOffset = 15;
    innerOffset = 10;
  } else if (offset < 5) {
    outerOffset = 5;
    innerOffset = 3;
  } else {
    outerOffset = offset;
    innerOffset = offset - (Math.ceil(offset / 5) + 1);
  }

  this.drawRect(p1, p2, { lineWidth, strokeColor, fillColor });
  this.drawCorner(
    { x: p1.x + outerOffset, y: p1.y + outerOffset },
    { x: p2.x - outerOffset, y: p2.y - outerOffset },
    {
      outerOffset: outerOffset,
      innerOffset: innerOffset,
      fillStyle: 'rgba(0,204,187,0.8)'
      // fillStyle: 'rgba(255,255,255,0.8)'
    }
  );
};

// 人体 Skeleton
HCanvas.prototype.drawBodyBox2 = function (p1, p2) {
  var lineWidth = 2;
  var strokeColor = 'rgba(255,255,255,0.4)';
  var fillColor = 'rgba(0,204,187,0.4)';

  var width = p2.x - p1.x;
  var height = p2.y - p1.y;
  var offset = Math.min(width / 12, height / 12);
  var outerOffset, innerOffset;

  if (offset >= 7) {
    outerOffset = 10;
    innerOffset = 7;
  } else if (offset < 7) {
    outerOffset = 5;
    innerOffset = 3;
  }

  this.drawRect(p1, p2, { lineWidth, strokeColor, fillColor });
  this.drawCorner(
    { x: p1.x + outerOffset, y: p1.y + outerOffset },
    { x: p2.x - outerOffset, y: p2.y - outerOffset },
    {
      outerOffset: outerOffset,
      innerOffset: innerOffset,
      fillStyle: 'rgba(255,255,255,0.8)'
    }
  );
};

HCanvas.prototype.drawBodyBoxMot = function (p1, p2) {
  var fillColor = 'rgba(42,210,194,0.30)';
  var strokeColor = 'rgba(0,208,187,1)';

  this.drawRect(p1, p2, { strokeColor, fillColor });
  // this.drawCorner(p1, p2);
};

HCanvas.prototype.drawBodyBoxId = function (p1, p2, id) {
  if (id == -1 || id == undefined) return;
  var context = this.context;
  var colorArr = ['#14CCBA', '#0066FF', '#F5A623', '#6DB324', '#9013FE'];
  var colorById = id % colorArr.length;
  var minW = 50;
  var boxW = Math.abs(p2.x - p1.x) / 2;
  var idBoxW = boxW > minW ? boxW : minW;
  var idBoxH = idBoxW * 0.4;
  var beginX = p1.x;
  var beginY = p1.y;
  var trapezoidArr = [
    { x: beginX, y: beginY },
    { x: beginX, y: beginY - idBoxH },
    { x: beginX + idBoxW, y: beginY - idBoxH },
    { x: beginX + idBoxW + idBoxH / 2, y: beginY }
  ];
  var fontstring = idBoxH * 0.6 + 'px Arial';

  context.beginPath();
  trapezoidArr.forEach((pos, i) => {
    if (i == 0) {
      context.moveTo(pos.x, pos.y);
    } else {
      context.lineTo(pos.x, pos.y);
    }
  });
  context.fillStyle = colorArr[colorById];
  context.fill();
  context.closePath();

  context.beginPath();
  context.fillStyle = '#ffffff';
  context.font = fontstring;
  // context.textAlign = 'left';
  context.textAlign = 'center';
  context.fillText(id, beginX + (idBoxW / 4) + (idBoxW + idBoxH / 2) / 4, beginY - idBoxH / 4);
  context.closePath();
};

HCanvas.prototype.drawAttributes = function (attributes, x, y) {
  var context = this.context;
  var fontstring = 40 + 'px Arial';
  context.beginPath();
  context.font = fontstring;
  context.textAlign = 'center';
  context.fillStyle = '#FFFFFFF';

  var text = '';
  // Object.keys(attributes).map(key => {
  //   text += `${key}:${attributes[key]};    `
  // });
  text += attributes['id'];
  // console.log(attributes, text, x, y);
  context.fillText(text, x, y);
  context.closePath();
};

HCanvas.prototype.drawHeadBox = function (p1, p2) {
  var lineWidth = 2;
  var strokeColor = '#0066FF';
  this.drawRect(p1, p2, { lineWidth, strokeColor });
};

HCanvas.prototype.drawBorderHeadBox = function (p1, p2, color = 'rgba(0,208,187,0.2)') {
  var lineWidth = 2;
  var strokeColor = color;
  this.drawRect(p1, p2, { lineWidth, strokeColor, fillColor: color });
  var context = this.context;
  context.beginPath();
  context.moveTo(p1.x, p1.y + 20);
  context.lineTo(p1.x, p1.y);
  context.lineTo(p1.x + 20, p1.y);

  context.moveTo(p2.x - 20, p1.y);
  context.lineTo(p2.x, p1.y);
  context.lineTo(p2.x, p1.y + 20);

  context.moveTo(p2.x, p2.y - 20);
  context.lineTo(p2.x, p2.y);
  context.lineTo(p2.x - 20, p2.y);

  context.moveTo(p1.x + 20, p2.y);
  context.lineTo(p1.x, p2.y);
  context.lineTo(p1.x, p2.y - 20);

  context.lineWidth = 4;
  context.strokeStyle = 'rgba(0,208,187,1)';
  // context.closePath();
  context.stroke();
};

HCanvas.prototype.drawHeadBoxByImage = function (p1, p2) {
  var headW = Math.abs(p2.x - p1.x) * 1.2;
  var headH = Math.abs(p2.y - p1.y) * 1.2;
  this.context.drawImage(this.imgs['headImage.png'], p1.x - (0.1 * headW), p1.y - (0.1 * headH), headW, headH);
};

HCanvas.prototype.drawFaceBox = function (p1, p2) {
  var lineWidth = 2;
  var strokeColor = '#F5222D';
  this.drawRect(p1, p2, { lineWidth, strokeColor });
};

HCanvas.prototype.drawOuntline = function (points) {
  this.drawLine();
};

HCanvas.prototype.drawSkeleton = function (points) {
  // 连接眼鼻
  var minScore = 0.3;
  if (
    points['leftEye'].score > minScore &&
    points['rightEye'].score > minScore
  ) {
    this.drawLine(points['leftEye'], points['rightEye'], {
      lineWidth: 2
    });
  }
  if (points['rightEye'].score > minScore && points['nose'].score > minScore) {
    this.drawLine(points['rightEye'], points['nose'], {
      lineWidth: 2
    });
  }
  if (points['nose'].score > minScore && points['leftEye'].score > minScore) {
    this.drawLine(points['nose'], points['leftEye'], {
      lineWidth: 2
    });
  }

  // 连接耳目
  if (
    points['leftEye'].score > minScore &&
    points['leftEar'].score > minScore
  ) {
    this.drawLine(points['leftEye'], points['leftEar'], {
      lineWidth: 2
    });
  }
  if (
    points['rightEye'].score > minScore &&
    points['rightEar'].score > minScore
  ) {
    this.drawLine(points['rightEye'], points['rightEar'], {
      lineWidth: 2
    });
  }

  // if (
  //   points['leftEye'].score > minScore &&
  //   points['rightEye'].score > minScore &&
  //   points['nose'].score > minScore &&
  //   points['leftEar'].score > minScore &&
  //   points['rightEar'].score > minScore
  // ) {
  var self = this;
  ['leftEye', 'rightEye', 'nose', 'leftEar', 'rightEar'].forEach(function (
    item
  ) {
    var point = points[item];
    if (point.score > minScore) {
      self.drawPoint(point.x, point.y, {
        radius: 3,
        lineWidth: 2
      });
    }
  });
  // }

  // 连接耳肩
  if (
    points['leftEar'].score > minScore &&
    points['leftShoulder'].score > minScore
  ) {
    this.drawLine(points['leftEar'], points['leftShoulder'], {
      lineWidth: 2
    });
  }
  if (
    points['rightEar'].score > minScore &&
    points['rightShoulder'].score > minScore
  ) {
    this.drawLine(points['rightEar'], points['rightShoulder'], {
      strokeColor: '#F8E71C',
      lineWidth: 2
    });
  }

  // 连接躯干
  if (
    points['leftShoulder'].score > minScore &&
    points['rightShoulder'].score > minScore
  ) {
    this.drawLine(points['leftShoulder'], points['rightShoulder']);
  }
  if (
    points['rightShoulder'].score > minScore &&
    points['rightHip'].score > minScore
  ) {
    this.drawLine(points['rightShoulder'], points['rightHip']);
  }
  if (
    points['rightHip'].score > minScore &&
    points['leftHip'].score > minScore
  ) {
    this.drawLine(points['rightHip'], points['leftHip']);
  }
  if (
    points['leftHip'].score > minScore &&
    points['leftShoulder'].score > minScore
  ) {
    this.drawLine(points['leftHip'], points['leftShoulder']);
  }

  // 连接上肢
  if (
    points['leftShoulder'].score > minScore &&
    points['leftElbow'].score > minScore
  ) {
    this.drawLine(points['leftShoulder'], points['leftElbow'], {
      strokeColor: '#06F'
    });
  }
  if (
    points['leftElbow'].score > minScore &&
    points['leftWrist'].score > minScore
  ) {
    this.drawLine(points['leftElbow'], points['leftWrist'], {
      strokeColor: '#0CB'
    });
  }
  if (
    points['leftEye'].score > minScore &&
    points['rightElbow'].score > minScore
  ) {
    this.drawLine(points['rightShoulder'], points['rightElbow'], {
      strokeColor: '#F5222D'
    });
  }
  if (
    points['rightElbow'].score > minScore &&
    points['rightWrist'].score > minScore
  ) {
    this.drawLine(points['rightElbow'], points['rightWrist'], {
      strokeColor: '#F5A623'
    });
  }

  // 连接下肢
  if (
    points['leftHip'].score > minScore &&
    points['leftKnee'].score > minScore
  ) {
    this.drawLine(points['leftHip'], points['leftKnee'], {
      strokeColor: '#06F'
    });
  }
  if (
    points['leftKnee'].score > minScore &&
    points['leftAnkle'].score > minScore
  ) {
    this.drawLine(points['leftKnee'], points['leftAnkle'], {
      strokeColor: '#0CB'
    });
  }
  if (
    points['rightHip'].score > minScore &&
    points['rightKnee'].score > minScore
  ) {
    this.drawLine(points['rightHip'], points['rightKnee'], {
      strokeColor: '#F5222D'
    });
  }
  if (
    points['rightKnee'].score > minScore &&
    points['rightAnkle'].score > minScore
  ) {
    this.drawLine(points['rightKnee'], points['rightAnkle'], {
      strokeColor: '#F5A623'
    });
  }

  var self = this;
  Object.keys(points).forEach(function (item) {
    if (['leftEye', 'rightEye', 'nose', 'leftEar', 'rightEar'].includes(item)) {
      return;
    }

    var point = points[item];
    if (point.score > minScore) {
      self.drawPoint(point.x, point.y, 5);
    }
  });
};

HCanvas.prototype.drawSegment = function (imageData, x, y) {
  var context = this.context;
  // var imageData = context.createImageData(width, height);

  // imageData.data = Uint8ClampedArray.from(imageDataArr);
  // // 上边的赋值方法无法绘制，先使用遍历的方法实现
  // for(var i = 0; i < imageData.data.length; i++) {
  //   imageData.data[i] = imageDataArr[i];
  // }

  context.putImageData(imageData, x, y);
};

/**
 * 绘制人体轮廓并填充（轮廓数据为相对数据，需加上绝对位置）
 */
HCanvas.prototype.drawSegmentBorder = function (imageData, x, y, color = 'rgba(255, 255, 0, 0.2)') {
  var ctx = this.context;
  ctx.beginPath();
  imageData.map((point, index) => {
    if (index === 0) {
      ctx.moveTo(point.x_ + x, point.y_ + y);
    } else {
      ctx.lineTo(point.x_ + x, point.y_ + y);
    }
  });
  ctx.fillStyle = color;
  ctx.strokeStyle = color;
  ctx.fill();
  ctx.stroke();
};

HCanvas.prototype.drawTimeStamp = function (time) {
  var context = this.context;
  var fontstring = 40 + 'px Arial';
  context.beginPath();
  context.fillStyle = 'red';
  context.font = fontstring;
  context.textAlign = 'left';
  context.fillText(time, 20, 40);
  context.closePath();
};

HCanvas.prototype.drawVehicle = function (p1, p2) {
  var strokeColor = 'rgba(255, 255, 255, 0.2)';
  var fillColor = 'rgba(0,204,187,0.3)';
  this.drawRect(p1, p2, { strokeColor, fillColor });
  this.drawCorner(
    { x: p1.x + 7, y: p1.y + 7 },
    { x: p2.x - 7, y: p2.y - 7 },
    {
      outerOffset: 7,
      innerOffset: 5,
      fillStyle: 'rgba(255,255,255,0.8)'
    }
  );
};

HCanvas.prototype.drawCyclist = function (p1, p2) {
  var strokeColor = 'rgba(255, 255, 255, 0.2)';
  var fillColor = 'rgba(0,102,255,0.3)';
  this.drawRect(p1, p2, { strokeColor, fillColor });
  this.drawCorner(
    { x: p1.x + 7, y: p1.y + 7 },
    { x: p2.x - 7, y: p2.y - 7 },
    {
      outerOffset: 7,
      innerOffset: 5,
      fillStyle: 'rgba(255,255,255,0.8)'
    }
  );
};

HCanvas.prototype.drawPedestrian = function (p1, p2) {
  var strokeColor = 'rgba(255, 255, 255, 0.2)';
  var fillColor = 'rgba(255,102,128,0.3)';
  this.drawRect(p1, p2, { strokeColor, fillColor });
  this.drawCorner(
    { x: p1.x + 7, y: p1.y + 7 },
    { x: p2.x - 7, y: p2.y - 7 },
    {
      outerOffset: 7,
      innerOffset: 5,
      fillStyle: 'rgba(255,255,255,0.8)'
    }
  );
};

HCanvas.prototype.drawPathArea = function (points, ratio, color) {
  var context = this.context;
  context.beginPath();
  points.forEach((point, index) => {
    var x = point.x * ratio.width;
    var y = point.y * ratio.height;
    if (index == 0) {
      // this.drawPoint(x, y, {});
      context.moveTo(x, y);
    } else {
      // this.drawPoint(x, y, {});
      context.lineTo(x, y);
    }
  });
  // context.lineTo(point)
  context.lineWidth = 3;
  context.strokeStyle = color;
  context.closePath();
  context.stroke();

  points.forEach(point => {
    var x = point.x * ratio.width;
    var y = point.y * ratio.height;
    this.drawPoint(x, y, {
      strokeColor: color,
      fillColor: color
    });
  });
};

// HCanvas.prototype.drawDynamicLine = function(points, options) {

// }

HCanvas.prototype.drawPath = function (points, ratio, color, id) {
  var context = this.context;
  // if (points) {
  context.beginPath();
  for (var i = 0; i < points.length; i++) {
    var x = points[i].x * ratio.width;
    var y = points[i].y * ratio.height;

    if (i == 0) {
      context.moveTo(x, y);
    } else {
      if (Math.abs(points[i - 1].x - points[i].x) > 100 || Math.abs(points[i - 1].y - points[i].y) > 100) {
        context.moveTo(x, y);
        if (i < points.length - 2 && (Math.abs(points[i + 1].x - points[i].x) > 100 || Math.abs(points[i + 1].y - points[i].y) > 100)) {
          var px = points[i + 1].x * ratio.width;
          var py = points[i + 1].y * ratio.height;
          context.moveTo(px, py);
        }
      } else {
        context.lineTo(x, y);
      }
    }
  }
  context.lineWidth = 3;
  context.strokeStyle = color;
  context.stroke();

  points.forEach((point, index) => {
    var x = point.x * ratio.width;
    var y = point.y * ratio.height;
    this.drawPoint(x, y, {
      strokeColor: color,
      fillColor: color
    });
    if (id && index == points.length - 1) {
      var fontstring = 20 + 'px Arial';
      context.beginPath();
      context.font = fontstring;
      context.textAlign = 'left';
      context.fillText(id, x, y);
      // context.fillStyle = '#FFFFFFF';
      context.closePath();
    }
  });
  // }
};

HCanvas.prototype.drawPathSmooth = function (points, ratio, color, smooth) {
  var context = this.context;
  // console.log(points)
  for (var i = 0; i < points.length; i + smooth) {
    // var = point[i]
    // console.log(i)
    if (i % smooth == 0) {
      var smoothPoint = points[i - smooth] || { x: 0, y: 0 };
      var x = points[i].x * ratio.width;
      var y = points[i].x * ratio.height;
      var sx = smoothPoint.x * ratio.width;
      var sy = smoothPoint.y * ratio.width;
      // console.log(x, y, sx, sy)
      if (i == 0) {
        context.moveTo(x, y);
      } else {
        var cx = (sx + x) / 2;
        var cy = (sy + y) / 2;
        context.quadraticCurveTo(sx, sy, cx, cy);
      }
    }
  }
  context.lineWidth = 3;
  context.strokeStyle = color;
  context.stroke();
};
