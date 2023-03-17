function RenderFrame(canvasObj, canvasOjb2, info1, info2, videoId, performance) {
  this.videoId = videoId;
  this.imgMain = document.getElementById(videoId);
  this.info1 = document.getElementById(info1);
  this.info2 = document.getElementById(info2);
  this.performance = document.getElementById(performance);
  this.smartCanvas1 = new HCanvas(canvasObj);
  this.smartCanvas2 = new HCanvas(canvasOjb2);
}

/**
 * 渲染页面
 * @param {*} frame
 */
RenderFrame.prototype.render = function (frame) {
  if (frame.imageBlob) {
    let obj = this.smartCanvas1.getImageWH()
    if (obj.w !== frame.imageWidth || obj.h !== frame.imageHeight) {
      this.smartCanvas1.changeImageWH(frame.imageWidth, frame.imageHeight);
      this.smartCanvas2.changeImageWH(frame.imageWidth, frame.imageHeight);
      changeImgShow(frame.imageWidth, frame.imageHeight);
    }
    this.canvasOffset = this.calculateOffset(frame.imageWidth, frame.imageHeight);
    var urlCreator = window.URL || window.webkitURL;
    var imageUrl = urlCreator.createObjectURL(frame.imageBlob);
    this.renderVideo(imageUrl, frame);
    setTimeout(function () {
      urlCreator.revokeObjectURL(imageUrl);
    }, 10);
    // requestAnimationFrame(() => {
    //   
    // });
  }
  if (frame.performance.length) {
    this.renderPerformance(frame.performance);
  }
}

/**
 * 渲染视频流
 * @param {*} imageUrl
 */

RenderFrame.prototype.renderVideo = function (imageUrl, frame) {
  var _this = this;
  this.imgMain.src = imageUrl;
  this.imgMain.onload = function () {
    _this.renderFrameStart(frame);
  }
}

// 性能数据
RenderFrame.prototype.renderPerformance = function (performance) {
  let html = '';
  performance.map((item) => {
    html += `${item['type_']}: ${item['valueString_']}&nbsp;&nbsp;&nbsp;`
  })
  this.performance.innerHTML = html;
}


RenderFrame.prototype.renderFrameStart = function ({ smartMsgData }) { // frame
  this.smartCanvas1.clear();
  this.smartCanvas2.clear();
  let htmls1 = '';
  let htmls2 = '';
  if (smartMsgData.length) {
    smartMsgData.map(item => {
      if (item) {
        if (item.boxes.length) {
          this.renderFrameBoxes(item.boxes, item.fall.fallShow);
          if (item.attributes && item.attributes.box) {
            htmls1 += this.renderAttributes(item.attributes, item.id);
          }
        }
        if (item.fall.fallShow) {
          htmls2 += this.createAlertHtml(item.fall);
        }
        if (item.points.length) {
          this.renderFramePoints(item.points);
        }
        if (item.segmentation.length) {
          this.segmentation(item.segmentation);
        }
      }
    })
  }
  this.info1.innerHTML = htmls1;
  this.info2.innerHTML = htmls2;
  // console.timeEnd('渲染计时器')
}

// 渲染轮廓框
RenderFrame.prototype.renderFrameBoxes = function (boxes, fall) {
  let color = undefined
  if (fall) {
    color = [254, 108, 113];
  }
  boxes.map(item => {
    // drawBodyBoxId
    this.smartCanvas1.drawBodyBox(item.p1, item.p2, color);
    // this.smartCanvas1.drawBodyBox(item.p1, item.p2, color,  id);
  })
}

// 渲染骨骼线
RenderFrame.prototype.renderFramePoints = function (points) {
  points.map(item => {
    switch (item.type) {
      case "hand_landmarks":
        this.smartCanvas1.drawHandSkeleton(item.skeletonPoints);
        break;
      case "corner":
        this.smartCanvas1.drawArcPoint(item.skeletonPoints, "#0ff");
        break;
      case "lmk_106pts":
        this.smartCanvas1.drawArcPoint(item.skeletonPoints, "#0ff", item.diameterSize);
        break;
      case "parking":
        this.smartCanvas1.drawParkingPoint(item.skeletonPoints);
        break;
      default:
        this.smartCanvas1.drawSkeleton(item.skeletonPoints);
        break;
    }
  })
}

RenderFrame.prototype.createTemplateAttributesHtml = function (attributes, id, className, top, left) {
  let html = `<li class="${className}" style="top:${top}; left:${left}"><ol>`
  if (typeof attributes.type !== 'undefined') {
    html += `<li class="${attributes.type}">${attributes.type}
      ${typeof id !== 'undefined' && id > 0 ? `: ${id}`: ''}
      ${typeof attributes.score !== 'undefined' && attributes.score > 0 ? `(${attributes.score.toFixed(3)})` : ''}
    </li>`
  }
  if (attributes.attributes.length) {
    attributes.attributes.map(val => {
      html += `<li class="${val.type}">${val.type}: <span class="${val.type === 'gesture' ? 'gesture' : ''}">${val.value || ''}</span>
        ${typeof val.score !== 'undefined' && val.score > 0 ? `(${val.score.toFixed(3)})` : ''}
      </li>`;
    });
  }
  html += '</ol></li>'
  return html;
}

// 计算canvas像素和屏幕像素之间的比例关系以及偏移量
RenderFrame.prototype.calculateOffset = function (width, height) {
  // const parentEle = this.imgMain.parentNode;
  const canvasWidth = this.imgMain.offsetWidth;
  const canvasHeight = this.imgMain.offsetHeight;

  // const canvasoffsetX = this.imgMain.offsetLeft + parentEle.offsetLeft;
  // const canvasoffsetY = this.imgMain.offsetTop + parentEle.offsetTop;

  const xScale = canvasWidth / width;
  const yScale = canvasHeight / height;
  return {
    xScale,
    yScale,
    // offsetX: canvasoffsetX,
    // offsetY: canvasoffsetY
  };
}

// 渲染属性框
RenderFrame.prototype.renderAttributes = function (attributes, id) {
  let box = attributes.box;
  let len = attributes.attributes.length;
  if (typeof attributes.type !== 'undefined') {
    len += 1;
  }
  let className = 'attribute-panel small';
  let left = box.p1.x * this.canvasOffset.xScale - 12
  let top = box.p1.y * this.canvasOffset.yScale;

  if (top - len * 40 >= 0) {
    top = top - len * 40
  }
  let html = this.createTemplateAttributesHtml(attributes, id, className, top + 'px', left + 'px');
  return html
}

RenderFrame.prototype.createTemplateAlertHtml = function (score, top, left) {
  let html = `<li class="alert" style="top:${top}; left:${left}">
    <p class="img"><img src="../assets/images/danger.png" width="16px" alt=""/>有人摔倒啦</p>
  `
  if (typeof score !== 'undefined' && score > 0) {
    html += `<p>score: ${score.toFixed(3)}</p>`;
  }
  html + `</li>`
  return html;
}

// 摔倒弹窗提示
RenderFrame.prototype.createAlertHtml = function (fall) {
  if (!fall.box) {
    return;
  }
  let box = fall.box
  let html = ''
  if (fall.value === 1) {
    if (box.p1.y <= 1) {
      return;
    }
    let x = box.p2.x * this.canvasOffset.yScale - box.p1.x * this.canvasOffset.yScale
    let left = box.p2.x * this.canvasOffset.xScale - x + 'px';
    let top = box.p1.y * this.canvasOffset.yScale - 3 + 'px';
    html = this.createTemplateAlertHtml(fall.score, top, left);
  }
  return html
}

// 分割
RenderFrame.prototype.segmentation = function (segmentation) {
  segmentation.map(item => {
    if (item.data && item.data.length) {
      if (item.type === 'full_img') {
        this.smartCanvas2.drawFloatMatrixs(item);
      } else if (item.type === 'target_img') {
        this.smartCanvas2.drawSegmentBorder(item.data, 'rgba(0, 255, 25, 0.5)');
      }
    }
  })
}

function changeImgShow(width, height) {
  window.onresize = function () { 
    changeImgShow(width, height);
    return;
  }
  const video = document.querySelector('.video');
  const cam = document.querySelectorAll('.cam');

  const widthRadio = video.offsetWidth / width
  const heihgtRadio = video.offsetHeight / height
  const ratio = widthRadio - heihgtRadio

  if (ratio < 0) {
    widths = '100%';
    heights = height * widthRadio + 'px';
  } else {
    widths = width * heihgtRadio + 'px'
    heights = '100%'
  }
  Array.from(cam).map((item) => {
    item.style.width = widths
    item.style.height = heights
  })
}