import pygame

def drawText(surface, text, font_size, color, center, angle, font_name=None):
    """
    Рисует повёрнутый текст на заданной поверхности, центрируя его относительно заданной точки.
    
    Параметры:
      surface   : pygame.Surface - поверхность, на которую рисуем текст.
      text      : str - текст для отображения.
      font_size : int - размер шрифта.
      color     : tuple - цвет текста (R, G, B).
      center    : tuple - координаты центра (x, y), относительно которого центрируется текст.
      angle     : float - угол поворота текста в градусах.
      font_name : str или None - путь к файлу шрифта или имя системного шрифта (по умолчанию None, используется системный шрифт).
    """

    if font_name:
        font = pygame.font.Font(font_name, font_size)
    else:
        font = pygame.font.SysFont(None, font_size)
    
    text_surface = font.render(text, True, color)
    
    rotated_surface = pygame.transform.rotate(text_surface, angle)
    
    rotated_rect = rotated_surface.get_rect(center=center)
    
    surface.blit(rotated_surface, rotated_rect)
