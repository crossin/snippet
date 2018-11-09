// Learn cc.Class:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/class.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/class.html
// Learn Attribute:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/reference/attributes.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/life-cycle-callbacks.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/life-cycle-callbacks.html

var Enemy = cc.Class({
    extends: cc.Component,

    properties: {
        speed: 0,
        speed_min: 0,
        speed_max: 0,
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad () {
        this.speed = Math.random() * (this.speed_max - this.speed_min) + this.speed_min;
        let w = this.game.screen_width - 80;
        this.node.setPosition(Math.random() * w - w / 2, 380);
    },

    start () {

    },
    
    onCollisionEnter: function (other, self) {
        self.node.destroy();
    },

    update (dt) {
        if (this.game.is_over || this.node.y < -400) {
            this.node.destroy();
        }
        this.node.y -= this.speed * dt * this.game.speed();
    },
});

