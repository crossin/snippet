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

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {},

    start () {

    },

    update (dt) {
        let w = this.game.screen_width / 2 - 40;
        if (this.node.x < -w) {
            this.node.x = -w;
        } else if (this.node.x > w) {
            this.node.x = w;
        }

        if (this.node.y < -320) {
            this.node.y = -320;
        } else if (this.node.y > 300) {
            this.node.y = 300;
        }
    },

    onCollisionEnter: function (other, self) {
        this.game.gameover();
        self.node.destroy();
    },
});
