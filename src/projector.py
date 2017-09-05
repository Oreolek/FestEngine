import wx


class ProjectorWindow(wx.Frame):
    def __init__(self, parent, screen=None):
        if screen is None:
            screen = wx.Display.GetCount() - 1
        origin_x, origin_y, self.w, self.h = wx.Display(screen).GetGeometry().Get()
        single_screen = wx.Display.GetCount() < 2

        wx.Frame.__init__(self, parent, pos=(origin_x + 60, origin_y + 60), size=(self.w - 120, self.h - 120),
                          title='Projector Window',
                          style=wx.DEFAULT_FRAME_STYLE | (0 if single_screen else wx.STAY_ON_TOP))
        self.SetBackgroundColour(wx.BLACK)

        self.sizer = wx.BoxSizer()

        self.video_panel = wx.Panel(self)
        self.video_panel.SetBackgroundColour(wx.BLACK)

        self.video_panel.Hide()

        class ImagesPanel(wx.Panel):
            def __init__(self, parent):
                wx.Panel.__init__(self, parent)

                self.SetBackgroundColour(wx.BLACK)
                #img = wx.Image("../logo.png", wx.BITMAP_TYPE_ANY)
                #w, h = img.GetWidth(), img.GetHeight()
                #max_w = parent.w
                #max_h = parent.h
                #target_ratio = min(max_w / float(w), max_h / float(h))
                #new_w, new_h = [int(x * target_ratio) for x in (w, h)]
                #img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
                #self.drawable_bitmap = img
                self.drawable_bitmap = wx.BitmapFromImage(wx.EmptyImage(parent.w, parent.h));
                self.SetBackgroundStyle(wx.BG_STYLE_ERASE)

                self.Bind(wx.EVT_SIZE, self.on_size)
                self.Bind(wx.EVT_PAINT, self.on_paint)
                self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

            def on_size(self, e):
                self.Layout()
                self.Refresh()

            def on_erase_background(self, e):
                pass  # https://github.com/Himura2la/FestEngine/issues/30

            def on_paint(self, e):
                dc = wx.BufferedPaintDC(self)
                w, h = self.GetClientSize()
                if not w or not h:
                    return
                dc.Clear()
                drw_w = self.drawable_bitmap.GetWidth()
                drw_h = self.drawable_bitmap.GetHeight()
                dc.DrawBitmap(
                    self.drawable_bitmap,
                    w//2 - drw_w//2,
                    h//2 - drw_h//2,
                )

        self.images_panel = ImagesPanel(self)
        self.sizer.Add(self.images_panel, 1, wx.EXPAND)
        self.sizer.Add(self.video_panel, 1, wx.EXPAND)  # TODO: Align top

        self.SetSizer(self.sizer)
        self.Layout()

        if not single_screen:
            self.ShowFullScreen(True, wx.FULLSCREEN_ALL)

    def load_zad(self, file_path, fit=True):
        img = wx.Image(file_path, wx.BITMAP_TYPE_ANY)
        if fit:
            w, h = img.GetWidth(), img.GetHeight()
            max_w, max_h = self.images_panel.GetSize()
            target_ratio = min(max_w / float(w), max_h / float(h))
            new_w, new_h = [int(x * target_ratio) for x in (w, h)]
            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
        self.images_panel.drawable_bitmap = wx.BitmapFromImage(img)
        self.images_panel.Refresh()

    def switch_to_video(self, e=None):
        self.video_panel.Show()
        self.images_panel.Hide()

    def switch_to_images(self, e=None):
        self.video_panel.Hide()
        self.images_panel.Show()

    def no_show(self):
        self.images_panel.drawable_bitmap = \
            wx.BitmapFromImage(wx.EmptyImage(*self.images_panel.drawable_bitmap.GetSize()))
        self.images_panel.Refresh()
