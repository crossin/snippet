// Learn cc.Class:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/class.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/class.html
// Learn Attribute:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/reference/attributes.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - [Chinese] http://docs.cocos.com/creator/manual/zh/scripting/life-cycle-callbacks.html
//  - [English] http://www.cocos2d-x.org/docs/creator/en/scripting/life-cycle-callbacks.html

cc.Class({
    extends: cc.Component,

    properties: {
        speed: 0,
    },

    // LIFE-CYCLE CALLBACKS:

    onLoad () {
    },

    start () {

    },

    onHit () {

    },

    onCollisionEnter: function (other, self) {
        this.game.gainScore();
        self.node.destroy();
    },

    update (dt) {
        if (this.game.is_over || this.node.y > 400) {
            this.node.destroy();
        }
        this.node.y += this.speed * dt;
    },
});
