import os
import random
import sys
import time
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


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上に
    「Game Over」の文字と、泣いているこうかとん画像を表示する
    引数 screen：画面Surface
    """
    # 黒い矩形を描画するための空のSurfaceを作る
    kuro_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(kuro_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    
    # 透明度を設定して、先に黒い幕だけscreenに貼り付ける
    kuro_img.set_alpha(127)
    screen.blit(kuro_img, (0, 0))
    
    # 白文字のSurfaceを作り、【screenに】貼り付ける
    fonto = pg.font.Font(None, 80)
    txt_img = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_img.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    screen.blit(txt_img, txt_rct)
    
    # こうかとん画像をロードし、【screenに】貼り付ける
    kk_img = pg.image.load("fig/8.png") 
    kk_rct = kk_img.get_rect()
    
    # 文字の左側に配置
    kk_rct.center = WIDTH // 2 - 200, HEIGHT // 2
    screen.blit(kk_img, kk_rct)
    
    # 文字の右側に配置
    kk_rct.center = WIDTH // 2 + 200, HEIGHT // 2
    screen.blit(kk_img, kk_rct)
    
    # 5. 画面を更新して5秒待つ
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の準備
    bb_imgs, bb_accs = init_bb_imgs()
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

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0])

        # こうかとん移動処理
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

        # 爆弾の拡大・加速処理
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
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