!function(w){
  var _jpkeyobj = {
    A :65,
    J :74,
    S :83,
    1 :49,
    B :66,
    K :75,
    T :84,
    2 :50,
    C :67,
    L :76,
    U :85,
    3 :51,
    D :68,
    M :77,
    V :86,
    4 :52,
    E :69,
    N :78,
    W :87,
    5 :53,
    F :70,
    O :79,
    X :88,
    6 :54,
    G :71,
    P :80,
    Y :89,
    7 :55,
    H :72,
    Q :81,
    Z :90,
    8 :56,
    I :73,
    R :82,
    0 :48,
    9 :57,
    'kg':32,
    'Shift':16,
    'Alt':18,
    'Ctrl':91,
    'up':38,
    'down':40,
    'left':37,
    'right':39,
    'tab':9,
    '~':192,
    '+':187,
    '-':189
  }


  function Eventfun(){
    this.keyobj = _jpkeyobj
    this.isdownfun = true

    this.isN = false
    this.isM = false

    this.isShift = false
    this.isAlt   = false

    this.init()
  }

  Eventfun.prototype.init = function(){
    var _this = this
    window.onkeydown = function(event){
      var e = event || window.event || arguments.callee.caller.arguments[0];
      if(e && e.keyCode){
        var key = _this.keyobjfun(e.keyCode)
        if(_this.isdownfun && _this.keydown()[key]){
            _this.keydown()[key](event)
        }
      }
    };

    window.onkeyup = function(event){
        var e = event || window.event || arguments.callee.caller.arguments[0];
        if(e && e.keyCode){
          var key = _this.keyobjfun(e.keyCode)
          if(_this.isdownfun && _this.keyup()[key]){
              _this.keyup()[key](event)
          }
        }
    };
  }

    Eventfun.prototype.keyobjfun = function(num){
    var key = null
    for(var i in this.keyobj){
      if(this.keyobj[i] == num){
      key = i
      }
    }
    return key
    }

  Eventfun.prototype.keydown = function(){
      var _this = this
      var num = 2
      var obj = {
        // 上一帧
        "Q":function(){
            g_showhide()
        }
      }
      return obj
  }

  Eventfun.prototype.keyup = function(){
      var _this = this
      return {
      }
  }

    function __stopDefault(e) {
        if ( e && e.preventDefault )
            e.preventDefault();
        else
            window.event.returnValue = false;
        return false;
    }


  w.eventfun = function (){
    return new Eventfun()
  }

}(window)

eventfun()