var RocketLayer = cc.Layer.extend({
    G: -9.8 * 0.005,
    F: 0,
    R: 0,
    over: false,
    wind: 0,

    ctor: function () {
        this._super();

        var size = cc.winSize;

        // back
        var layerBack = new cc.Sprite(res.back_jpg);
        layerBack.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(layerBack);

        // rocket
        this.rocket = new cc.Sprite(res.rocket_png);
        this.addChild(this.rocket, 999);

        // flame
        this.flame = new cc.Sprite(res.flame_png);
        this.addChild(this.flame, 888);

        // platform
        this.platform = new cc.Sprite(res.platform_png);
        this.addChild(this.platform, 777);

        // label
        this.text = new cc.LabelTTF("成功降落！\n\n点击重新开始", "STHeiti", 30);
        this.text.attr({
            x: size.width / 2,
            y: size.height / 2,
        });
        this.addChild(this.text, 1111);

        this.text_wind = new cc.LabelTTF("", "STHeiti", 30);
        this.text_wind.attr({
            x: 100,
            y: size.height - 100,
        });
        this.addChild(this.text_wind, 100);

        this.init();

        this.scheduleUpdate();

    	// touch event
    	cc.eventManager.addListener({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            swallowTouches: true,
            onTouchBegan: this.onTouchBegan,
            onTouchMoved: this.onTouchMoved,
            onTouchEnded: this.onTouchEnded
        }, this);

        cc.eventManager.addListener({
            event: cc.EventListener.KEYBOARD,
            onKeyPressed:  this.onKeyPressed,
            onKeyReleased: this.onKeyReleased
        }, this);

        return true;
    },

    init: function (data) {
        var size = cc.winSize;
        this.rocket.attr({
            x: size.width / 2 + Math.random() * 200 - 100,
            y: size.height / 2 + 300,
            speed_x: 0,
            speed_y: 0,
            rotation: 0,
        });
        this.platform.attr({
            x: size.width / 2 + Math.random() * 400 - 200,
            y: 50,
        });
        this.flame.visible = false;
        this.text.visible = false;
        this.wind = Math.random() * 2 - 1;
        this.text_wind.setString('风速：' + (this.wind > 0 ? '→' : '←') + Math.abs(this.wind * 10).toFixed(2));
        this.over = false;
    },

    end: function (win=true) {
        if (win) {
            this.text.setString('    成功降落！\n\n点击重新开始')
            this.text.setColor(cc.color(20, 250, 20));
        } else {
            this.text.setString('    降落失败！\n\n点击重新开始')
            this.text.setColor(cc.color(250, 20, 20));
        }
        this.text.visible = true;
        this.over = true;
        this.cd = 1;
    },

    update: function (dt) {
        if (this.over) {
            this.cd -= dt;
            return;
        }

        var rocket = this.rocket;
        rocket.speed_y += this.G;

        var f_x = Math.sin(Math.PI / 180 * rocket.rotation);
        var f_y = Math.cos(Math.PI / 180 * rocket.rotation);
        rocket.speed_x *= 1.001;
        rocket.speed_x += f_x * this.F;
        rocket.speed_y += f_y * this.F;

        rocket.x += (rocket.speed_x + this.wind) * dt * 60;
        rocket.y += rocket.speed_y * dt * 60;
        rocket.rotation += this.R;

        this.flame.x = rocket.x
        this.flame.y = rocket.y
        this.flame.rotation = rocket.rotation

        // check win/lose
        if (rocket.y < 140 && Math.abs(rocket.x - this.platform.x) < this.platform.width / 2) {
            if (Math.abs(rocket.speed_x + this.wind) < 2 && Math.abs(rocket.speed_y) < 3 && Math.abs(rocket.rotation) < 10) {
                this.end(true);
            } else {
                this.end(false);
            }
        } else if (rocket.y < 40 || rocket.x < 0 || rocket.x > cc.winSize.width) {
            this.end(false);
        }
    },

    onTouchBegan: function (touch, event) {
        var self = event.getCurrentTarget();
        if (!self.over) {
            var pos = touch.getLocation();
            if (pos.x < cc.winSize.width / 2 - 100) {
                self.R = -0.25;
            } else if (pos.x > cc.winSize.width / 2 + 100) {
                self.R = 0.25;
            } else {
                self.F = 20 * 0.005;
                self.flame.visible = true;
            }
        }
        return true;
    },
    onTouchMoved: function (touch, event) {
    },
    onTouchEnded: function (touch, event) {
    	var self = event.getCurrentTarget();
        if (self.over && self.cd < 0) {
            self.init();
        }
        self.F = 0;
        self.R = 0;
        self.flame.visible = false;
    },

    onKeyPressed: function (keyCode, event) {
        var self = event.getCurrentTarget();
        if (!self.over) {
            if (keyCode == 37) {
                self.R = -0.25;
            } else if (keyCode == 39) {
                self.R = 0.25;
            } else {
                self.F = 20 * 0.005;
                self.flame.visible = true;
            }
        }
        return true;
    },
    onKeyReleased: function (keyCode, event) {
        var self = event.getCurrentTarget();
        if (self.over && self.cd < 0) {
            self.init();
        }
        self.F = 0;
        self.R = 0;
        self.flame.visible = false;
    },

});

