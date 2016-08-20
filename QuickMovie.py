import wx
import lxml
from wx import xrc
from MovieData import MovieData
from Person import Person

class MyApp(wx.App):
    dictCast = {}
    
    def OnInit(self):
        self.res = xrc.XmlResource('QuickMovie.xrc')
        self.init_frame()
        return(True)

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frameMain')
        
        self.favicon = wx.Icon('film.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        self.frame.SetIcon(self.favicon)    
        self.statusBar = xrc.XRCCTRL(self.frame, 'statusBar')
         
        # Bind Controls
        self.cboTitle = xrc.XRCCTRL(self.frame, 'cboTitle')
        self.listCast = xrc.XRCCTRL(self.frame, 'listCast')
        self.txtYear = xrc.XRCCTRL(self.frame, 'txtYear')
        self.txtDirector = xrc.XRCCTRL(self.frame, 'txtDirector')
        self.txtRuntime = xrc.XRCCTRL(self.frame, 'txtRuntime')
        self.txtPlot = xrc.XRCCTRL(self.frame, 'txtPlot')
        self.btnSearch = xrc.XRCCTRL(self.frame, 'btnSearch')
        self.btnExit = xrc.XRCCTRL(self.frame, 'wxID_EXIT')

        # Bind Events
        self.frame.Bind(wx.EVT_BUTTON, self.OnClose, id=xrc.XRCID('wxID_EXIT'))
        self.frame.Bind(wx.EVT_CLOSE, self.OnExitApp)
        self.Bind(wx.EVT_BUTTON, self.OnSearchClick, self.btnSearch)
        self.cboTitle.Bind(wx.EVT_KEY_DOWN, self.OnTitleChange)
        self.cboTitle.Bind(wx.EVT_COMBOBOX, self.OnComboTitles, id=xrc.XRCID('cboTitle'))
        self.listCast.Bind(wx.EVT_LISTBOX, self.OnListCast, id=xrc.XRCID('listCast'))
        self.statusBar.SetStatusText('Ready')
        
        self.movieData = MovieData()
        self.frame.Show()
        
    def search_movie (self, title):
        print "**** In search_movie ****"
        self.set_wait_state(True)
        
        # Search for a movie (get a list of Movie objects).
        try:
            s_result = self.movieData.search_movie_data(title)
        except Exception, e:
            set_wait_state(False)
            # TODO
            print "Search failed"
            return
        
        index_count = 0
        self.cboTitle.Clear()
        
        for title in s_result:
            try:
                self.cboTitle.Append("%s, %s" % (title, title['year']))
            except Exception, e:
                print "year not found"               
                self.cboTitle.Append("%s" % (title))
                
            index_count += 1                    
        
        # For now, only display in the first result
        movie = s_result[0]
        self.movieData.update_movie_data(movie)
        
        self.load_fields(movie)
        self.set_wait_state(False)
        
    def load_fields(self, result):
        try:
            self.cboTitle.SetValue('%s' % result['title'])
        except Exception, e:
            print "title not found"        
        try:
            self.txtYear.SetValue('%s' % result['year'])
        except Exception, e:
            print "year not found"        
        try:
            self.txtDirector.SetValue('%s' % result['director'][0])
        except Exception, e:
            print "director not found"        
        try:
            self.txtRuntime.SetValue('%s min' % result['runtimes'][0])
        except Exception, e:
            print "runtime not found"        
        try:
            self.txtPlot.SetValue('%s' % result['plot outline'])
        except Exception, e:
            print "plot not found"        
        
        index_count = 0
        try:
            for person in result['cast']:
                self.listCast.Append('%s' % person['name'])
                # Save for when cast is clicked
                self.dictCast[index_count] = person.personID
                index_count += 1                    
        except Exception, e:
            print "cast not found"           
            
        # This fixed title not showing in combo
        # Set to the first item
        self.cboTitle.SetSelection(0)
            
    def clear_fields(self):
        self.txtDirector.Clear()
        self.txtRuntime.Clear()
        self.txtPlot.Clear()
        self.txtYear.Clear()
        self.listCast.Clear()
         
    def OnSearchClick(self, event): 
        self.title = self.cboTitle.GetValue()
        if self.title == '':
            self.statusBar.SetStatusText("Title is required")
            self.cboTitle.SetFocus()       
        else:
            # self.cboTitle.Clear()
            self.search_movie(self.title)
     
    def OnTitleChange(self, event): 
        # Clear all other fields if title is changed and director is not already empty
        if self.txtDirector <> '':
            self.clear_fields()
        event.Skip()    
        
    def OnComboTitles(self, event):
        print "**** In OnComboTitles ****"
        self.title = self.cboTitle.GetValue()
        
        # Remove comma and date
        self.title = self.title.rsplit(',', 1)[0]
        print self.title
        
        self.clear_fields()
        self.search_movie(self.title)
        
    def OnListCast(self, event):
        self.set_wait_state(True)
        
        selected = self.listCast.GetSelection()
        personID = self.dictCast[selected]
        
        s_result = self.movieData.get_person_data(personID)
        self.person = Person(s_result)
        
        self.set_wait_state(False)
    
    def set_wait_state(self, state):
        if state == True:
            myCursor= wx.StockCursor(wx.CURSOR_WAIT)
            self.frame.SetCursor(myCursor)
            self.statusBar.SetStatusText('Searching ...')            
        else:
            myCursor= wx.StockCursor(wx.CURSOR_ARROW)
            self.frame.SetCursor(myCursor)            
            self.statusBar.SetStatusText('Ready')               
    
    def OnClose(self, evt):
        self.Exit()
        
    def OnExitApp(self, event):
        self.Exit()
        
if __name__ == '__main__':
    # The False argument says redirect stdout/stderr to a console instead of a window
    app = MyApp(False)
    app.MainLoop()