// Learn cc.Class:
//  - https://docs.cocos.com/creator/manual/en/scripting/class.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

cc.Class({
    extends: cc.Component,

    properties: {
        change5: cc.Node,
        up: cc.Node,
        ret: cc.Node,
        borer: cc.Node,
        soil: cc.Node,
        flag: cc.Node,
        output: cc.RichText,
        ending: cc.Node,

        G: -0.01,
        F: 0,
        R: 0,
        phase: 1,
        ticks: 0,

        // foo: {
        //     // ATTRIBUTES:
        //     default: null,        // The default value will be used only when the component attaching
        //                           // to a node for the first time
        //     type: cc.SpriteFrame, // optional, default is typeof default
        //     serializable: true,   // optional, default is true
        // },
        // bar: {
        //     get () {
        //         return this._bar;
        //     },
        //     set (value) {
        //         this._bar = value;
        //     }
        // },
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad () {
        cc.debug.setDisplayStats(false);

        this.node.on(cc.Node.EventType.TOUCH_START, this.onTouchStart, this);
        this.node.on(cc.Node.EventType.TOUCH_END, this.onTouchEnd, this);   

        this.output.string = "1. 月面着陆\n<color=#88ffff>点击屏幕中部：点火减速\n点击屏幕两侧：调整姿态\n注意控制着落时的速度和角度</c>\n";
    },

    start () {

    },

    onTouchStart (event) {
        var pos = event.getLocation();
        if (pos.x < cc.winSize.width / 2 - 100) {
            this.R = 0.25;
        } else if (pos.x > cc.winSize.width / 2 + 100) {
            this.R = -0.25;
        } else {
            this.F = 10 * 0.005;
        }
    },
    onTouchEnd (event) {
        this.F = 0;
        this.R = 0;

        if (this.phase == 4 && this.ticks > 1) {
            cc.game.restart();
        }
    },

    update (dt) {
        if (this.phase == 1) {
            if (Math.abs(this.change5.x) > 300 || Math.abs(this.change5.y) > 500) {
                this.phase = 4;
                this.output.string += "<color=#ff8888>偏离目标区域太远，着陆失败！</c>\n点击屏幕再次尝试";
            }
            if (this.change5.y < -300) {
                var c5 = this.change5.getComponent('change5');
                if (Math.abs(c5.speed_x) > 1 || Math.abs(c5.speed_y) > 1) {
                    this.phase = 4;
                    this.output.string += "<color=#ff8888>速度太快，着陆失败！</c>\n点击屏幕再次尝试";
                } else if (Math.abs(this.change5.rotation) > 30) {
                    this.phase = 4;
                    this.output.string += "<color=#ff8888>角度太大，着陆失败！</c>\n点击屏幕再次尝试";
                } else {
                    this.phase = 2;
                    this.output.string += "<color=#88ff88>着陆成功！</c>\n\n2. 月壤采集工作中\n";
                    this.land();                    
                }
            }
        } else if (this.phase == 3) {
            if (Math.abs(this.up.x) > 300 || Math.abs(this.up.y) > 500) {
                this.phase = 4;
                this.output.string += "<color=#ff8888>偏离轨道器太远，对接失败！</c>\n点击屏幕再次尝试";                
            }
            if (Math.abs(this.up.y-this.ret.y)<10 && Math.abs(this.up.x-this.ret.x)<10) {
                var up = this.up.getComponent('up');
                var ret = this.ret.getComponent('return');
                if (Math.abs(up.speed_x-0.5) > 1 || Math.abs(up.speed_y) > 1) {
                    this.output.string += "<color=#ff8888>速度太快，对接失败！</c>\n点击屏幕再次尝试";
                } else if (Math.abs(this.change5.rotation) > 30) {
                    this.output.string += "<color=#ff8888>角度太大，对接失败！</c>\n点击屏幕再次尝试";
                } else {
                    this.output.string += "<color=#88ff88>对接成功！</c>\n任务完成";
                    this.ending.runAction(cc.fadeIn(1));
                }
                this.phase = 4;
            }
        } else if (this.phase == 4) {
            this.ticks += dt;
        }
    },

    land () {
        var c5 = this.change5;
        if (c5.angle == 0) {
            this.bore1();
        } else {
            // 此段为落地后的调整动画，可略过
            var dx = c5.width * 0.23 * Math.cos(Math.PI / 180 * c5.angle);
            var dy = c5.width * 0.23 * Math.sin(Math.PI / 180 * c5.angle);
            if (c5.angle < 0) {
                c5.anchorX = 0.73;
                c5.x += dx;
                c5.y += dy;
            } else {
                c5.anchorX = 0.27;
                c5.x -= dx;
                c5.y -= dy;
            }
            for (var i = c5.children.length - 1; i >= 0; i--) {
                var item = c5.children[i];
                var sign = c5.anchorX > 0.5 ? -1 : 1;
                item.x += sign * c5.width * 0.23;
            }
            var a1 = cc.rotateTo(Math.abs(c5.angle/45), 0);
            var a2 = cc.callFunc(this.bore1, this);
            c5.runAction(cc.sequence(a1, a2));
        }
    },

    bore1 () {
        this.borer.opacity = 255;
        var a1 = cc.scaleTo(2, 1, 20);
        var a2 = cc.callFunc(this.bore2, this);
        this.borer.runAction(cc.sequence(cc.delayTime(1), a1, cc.delayTime(1), a2));
    },

    bore2 () {
        var a1 = cc.scaleTo(2, 1, 20);
        this.soil.y = this.borer.y - this.borer.height * this.borer.scaleY;
        this.soil.opacity = 255;
        var a2 = cc.callFunc(this.bore3, this);        
        this.soil.runAction(cc.sequence(a1, cc.delayTime(2), a2));
    },

    bore3 () {
        var a1 = cc.scaleTo(2, 1, 0.1);
        this.soil.anchorY = 1;
        this.soil.y = this.borer.y;
        var a2 = cc.callFunc(this.flag1, this);
        this.soil.runAction(cc.sequence(a1, cc.delayTime(1), a2));
    },

    flag1 () {
        this.flag.opacity = 255;
        var a1 = cc.rotateTo(1, 360);
        var a2 = cc.callFunc(this.flag2, this);
        this.flag.runAction(cc.sequence(a1, a2));
    },

    flag2 () {
        this.phase = 3;
        this.output.string += "<color=#88ff88>采集完毕！</c>\n\n3. 月面上升\n<color=#88ffff>点击屏幕中部：点火上升\n点击屏幕两侧：调整姿态\n注意控制对接时的速度和角度</c>\n";
    },

    restart () {

    }
});
