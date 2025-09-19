import inkex, inspect
from inkex import TextElement, Page, Transform, Polygon, Layer, Rectangle, Group


class TiledPDF(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--grid_x', type=int, default='2',
            dest='grid_x', help="Number of pages in width")
        pars.add_argument('--grid_y', type=int, default='2',
            dest='grid_y', help="Number of pages in height")
        pars.add_argument('--overlap_x', type=float, default='20',
            dest='overlap_x', help="Overlapping left and right")
        pars.add_argument('--overlap_y', type=float, default='20',
            dest='overlap_y', help="Overlapping top and bottom")
        pars.add_argument('--borderwidth', type=float, default='0.5',
            dest='borderwidth', help="Borderwidth")
        pars.add_argument('--fontsize', type=int, default='32',
            dest='fontsize', help="Fontsize")
        pars.add_argument('--color_border', type=str, default='#7f7f7f',
            dest='color_border', help="Font- and bordercolor")

        pars.add_argument('--tab', type=str, default='', dest='', help="")
        pars.add_argument('--help_text', type=str, default='', dest='', help="")

    def effect(self):

        grid_x = self.options.grid_x
        grid_y = self.options.grid_y
        overlap_x = self.options.overlap_x
        overlap_y = self.options.overlap_y

        color = '#'+str(hex(int(self.options.color_border)))[2:8]
        alpha = int(str(hex(int(self.options.color_border)))[8:10],16)/255
        #inkex.utils.debug(color)
        #inkex.utils.debug(alpha)
        
        first_page = self.create_pages(grid_x, grid_y, overlap_x, overlap_y)

        layer_old = self.find_layer_by_label('pages')
        if layer_old != None:
            self.document.getroot().remove(layer_old)
            #inkex.utils.debug('found layer')
        
        page_num = 0
        #layer = self.svg.get_current_layer()
        layer = Layer.new(name='pages', label='pages')
        
        current_layer = self.svg.get_current_layer()
        # Find index of current layer
        children = list(self.document.getroot())
        try:
            index = children.index(current_layer)
            self.document.getroot().insert(index, layer)  # Insert before current layer
        except ValueError:
            root.append(layer)  # Fallback if current layer not found
        
        #self.document.getroot().append(layer)
        
        for y in range(grid_y):
            for x in range(grid_x):
                if x != 0:
                    ox = x*(first_page.width) - (x-1)*overlap_x
                    rx = x*(first_page.width) - (x-1)*overlap_x - overlap_x / 2
                else:
                    ox = overlap_x
                    rx = overlap_x / 2

                if y != 0:    
                    oy = (y+1) * (first_page.height - overlap_y)
                    ry = y * (first_page.height) - (y-1)*overlap_y - overlap_y / 2
                else:
                    oy = (y+1) * (first_page.height - overlap_y)
                    ry = overlap_y / 2

                page_num = page_num+1
                txt = str(page_num) + " ( x: " + str(x+1) + "| y: " + str(y+1) + " )"
                layer.add(self.add_text(ox, oy, txt, color, alpha))
                layer.add(self.add_rectangle(rx, ry, first_page.width-overlap_x, first_page.height-overlap_y, color, alpha))

    def create_pages(self, grid_x, grid_y, overlap_x, overlap_y):

        pages = self.svg.namedview.get_pages()
        first_page = pages[0]

        if len(pages) > 1:
            for p in range(len(pages)):
                if p > 0:
                    self.svg.namedview.remove(pages[p])
                
        for y in range(grid_y):
            for x in range(grid_x):
                if x != 0 or y != 0:
                    if x!=0:
                        ox = x*(first_page.width - overlap_x)
                    else:
                        ox = 0
                    
                    if y!=0:
                        oy = y*(first_page.height - overlap_y)
                    else:
                        oy = 0
                    
                    self.svg.namedview.new_page(str(ox), str(oy), str(first_page.width), str(first_page.height))

        return first_page
    
    def add_text(self, x, y, text, color, alpha):
        """Add a text label at the given location"""
        elem = TextElement(x=str(x), y=str(y))
        elem.text = str(text)
        elem.style = {
            'font-size': self.svg.unittouu(str(self.options.fontsize)+'pt'),
            'fill': color,
            'fill-opacity': str(alpha),
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal' }

        return elem

    def add_rectangle(self, x, y, w, h, color, alpha):
        elem = Rectangle(x=str(x), y=str(y), width=str(w), height=str(h))
        elem.style = {
            'fill': 'none',
            'stroke': color,
            'stroke-opacity': str(alpha),
            'stroke-width': str(self.options.borderwidth),
            'stroke-dasharray': '5,5'}

        return elem
    
    def find_layer_by_label(self, label):
            for node in self.document.getroot():
                if node.tag == inkex.addNS('g', 'svg') and node.get(inkex.addNS('groupmode', 'inkscape')) == 'layer':
                    if node.get(inkex.addNS('label', 'inkscape')) == label:
                        return node
            return None

if __name__ == '__main__':
    TiledPDF().run()
