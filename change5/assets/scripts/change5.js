// Learn cc.Class:
//  - https://docs.cocos.com/creator/manual/en/scripting/class.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

cc.Class({
    extends: cc.Component,

    properties: {
        speed_x: 0,
        speed_y: 0,
        flame: cc.Node,
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
        this.ctrl = this.node.parent.getComponent('Controller');
        this.flame.opacity = 0;
    },

    start () {

    },

    update (dt) {
        if (this.ctrl.phase == 1) {
            var change = this.node;
            this.speed_y += this.ctrl.G;

            var f_x = Math.sin(-Math.PI / 180 * change.angle);
            var f_y = Math.cos(Math.PI / 180 * change.angle);
            this.speed_x *= 1.001;
            this.speed_x += f_x * this.ctrl.F;
            this.speed_y += f_y * this.ctrl.F;

            change.x += this.speed_x * dt * 60;
            change.y += this.speed_y * dt * 60;
            change.angle += this.ctrl.R;

            if (this.ctrl.F > 0) {
                this.flame.opacity = 255;
            } else {
                this.flame.opacity = 0;
            }
        } else {
            this.flame.opacity = 0;
        }
    },
});
