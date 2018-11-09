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
        enemyPrefab: {
            default: null,
            type: cc.Prefab
        },

        planePrefab: {
            default: null,
            type: cc.Prefab
        },

        scoreDisplay: {
            default: null,
            type: cc.Label
        },
        timeDisplay: {
            default: null,
            type: cc.Label
        },

        resultDisplay: {
            default: null,
            type: cc.Sprite
        },
        rankDisplay: {
            default: null,
            type: cc.Sprite
        },
        scoreDisplay2: {
            default: null,
            type: cc.Label
        },
        nameBox: {
            default: null,
            type: cc.EditBox
        },
        msgBox: {
            default: null,
            type: cc.Label
        },
        current: {
            default: null,
            type: cc.Label
        },
        top10Box: {
            default: null,
            type: cc.Label
        },

        bulletPrefab: {
            default: null,
            type: cc.Prefab
        },
        interval: 0,
        time_lapsed: 0,

        enemyPrefab: {
            default: null,
            type: cc.Prefab
        },
        dogePrefab: {
            default: null,
            type: cc.Prefab
        },
        scallionPrefab: {
            default: null,
            type: cc.Prefab
        },
        interval_enemy: 0,
        is_over: false,
        score: 0,
        up_time: 0,
        total_time: 60,
        has_uped: false,
    },

    begin: function () {
        this.is_over = false;
        this.score = 0;
        this.up_time = 0;
        this.total_time = 60;
        this.has_uped = false,
        this.msgBox.string = '';
        this.scoreDisplay.string = 'Score: ' + this.score;

        this.resultDisplay.node.active = false;
        this.rankDisplay.node.active = false;

        var p = cc.instantiate(this.planePrefab);
        this.node.addChild(p, cc.macro.MAX_ZINDEX);
        p.getComponent('sicong').game = this;
        p.y = -200
        this.plane = p;

        this.node.on(cc.Node.EventType.TOUCH_MOVE, this.fly, this);
        // this.node.off(cc.Node.EventType.TOUCH_START, this.begin, this);
    },

    fly: function (event) {
        var delta = event.getDelta();
        this.plane.x += delta.x;
        this.plane.y += delta.y;
    },

    gainScore: function () {
        this.score += 1;
        this.scoreDisplay.string = 'Score: ' + this.score;
    },
    // LIFE-CYCLE CALLBACKS:

    onLoad () {
        var manager = cc.director.getCollisionManager();
        manager.enabled = true;
        let size = cc.view.getVisibleSize();
        this.screen_width = Math.min(size.width, 450);
        this.scoreDisplay.node.zIndex = cc.macro.MAX_ZINDEX;
        this.begin();

    },

    start () {

    },

    fire: function() {
        var bl = cc.instantiate(this.bulletPrefab);
        this.node.addChild(bl);
        bl.getComponent('bullet').game = this;
        bl.setPosition(this.plane.getPosition());
    },

    spawnEnemy: function() {
        var en;
        if (Math.random() < 0.05) {
            en = cc.instantiate(this.scallionPrefab);
            en.getComponent('scallion').game = this;    
        } else if (Math.random() < 0.3) {
            en = cc.instantiate(this.dogePrefab);
            en.getComponent('doge').game = this;                
        } else {
            en = cc.instantiate(this.enemyPrefab);
            en.getComponent('hotdog').game = this;                
        }
        en.getComponent('enemy').game = this;    
        this.node.addChild(en);
    },

    speedup: function() {
        this.up_time = 5;
    },

    speed: function() {
        if (this.up_time > 0) {
            return 3;
        } else {
            return 1;
        }
    },

    show_rank: function () {
        this.resultDisplay.node.active = false;
        this.rankDisplay.node.active = true;

        // get_rank
        var xhr = new XMLHttpRequest();
        var url = 'http://ppx.crossincode.com/top/?tag=wsc&score=' + this.score;
        xhr.game = this;
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var data = JSON.parse(xhr.responseText)
                this.game.current.string = data['rank'];
                var r_list = data['today'];
                var top_10 = '';
                for ( var i = 0; i < r_list.length; i++){
                    var kv = r_list[i];
                    var n = kv['name'];
                    top_10 += (i + '. ' + n + Array(18-n.length).join(' ') + kv['score'] + '\n')
                }
                this.game.top10Box.string = top_10;
            }
        };
        xhr.open("GET", url, true);
        xhr.send();
    },

    upload: function () {
        if (this.has_uped) {
            this.msgBox.string = '上传成功';
            return;
        }
        if (this.nameBox.string == '') {
            this.msgBox.string = '请输入昵称';
            return;
        }
        var xhr = new XMLHttpRequest();
        var url = 'http://ppx.crossincode.com/record/?name=' + this.nameBox.string + '&score=' + this.score + '&tag=wsc';
        xhr.game = this;
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                this.game.has_uped = true;
                this.game.msgBox.string = '上传成功';
            }
        };
        xhr.open("GET", url, true);
        xhr.send();
    },

    gameover: function () {
        this.plane.destroy();
        this.is_over = true;
        this.node.off(cc.Node.EventType.TOUCH_MOVE, this.fly, this);
        // this.node.on(cc.Node.EventType.TOUCH_START, this.begin, this);

        this.resultDisplay.node.active = true;
        this.scoreDisplay2.string = this.score;

        this.scoreDisplay.string = '';
        this.timeDisplay.string = '';
    },

    update (dt) {
        if (!this.is_over) {
            this.up_time -= dt;
            this.total_time -= dt;

            if (this.total_time < 0) {
                this.gameover();
                return;
            }

            // 发射子弹
            // this.time_lapsed += dt;
            // if (this.time_lapsed > this.interval) {
            //     this.time_lapsed = 0;
            //     this.fire();
            // }

            // 产生敌机
            this.interval_enemy -= dt * this.speed();
            if (this.interval_enemy < 0) {
                this.interval_enemy = Math.random() * 0.5 + 0.1;
                this.spawnEnemy();
            }

            this.timeDisplay.string = parseInt(this.total_time + 1);
        }
    },
});
