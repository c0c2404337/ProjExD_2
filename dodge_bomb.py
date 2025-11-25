import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向のはみだしチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向のはみだしチェック
        tate = False
    return yoko, tate


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを10段階準備する
    戻り値：爆弾Surfaceのリスト, 加速度のリスト
    """
    imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]
    return imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    
    bb_imgs, bb_accs = init_bb_imgs()
    
    # 最初の爆弾（サイズ1）を設定
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    vx, vy = +5, +5  # 爆弾の基本速度
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        
        # 現在の段階の画像と加速度を適用
        bb_img = bb_imgs[min(tmr // 500, 9)]
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]

        # 爆弾のサイズが変わったため、Rectの幅と高さを更新する
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        # 加速した速度で移動
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
            
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()