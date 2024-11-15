from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock

# class in which we are creating the canvas
class CanvasWidget(Widget):
     
    def __init__(self, **kwargs):
 
        super(CanvasWidget, self).__init__(**kwargs)
 
        # Arranging Canvas
        with self.canvas:
 
            Color(1, 1, 1, 1)  # set the colour 
 
            # Setting the size and position of canvas
            self.rect = Rectangle(pos = self.center,
                                  size =(self.width / 2.,
                                        self.height / 2.))
 
            # Update the canvas as the screen size change
            self.bind(pos = self.update_rect,
                  size = self.update_rect)
 
    # update function which makes the canvas adjustable.
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size





# The Login Screen
#   This is the first screen that a user will encounter when opening the app
#   Once the user enters their nuid, they can hit the login button to continue to the app
class LoginScreen(FloatLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(CanvasWidget())

        # Image
        self.add_widget(Image(
                               source="pack.png",
                               size=(500, 500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.85}
                               ))
        
        # Right Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.95, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
        # Left Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.05, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))

        # Text display instructing the user the enter their NUID
        self.greeting = Label(
                             text="Please Enter your NUID Below",
                             font_size = 18,
                             color='#000000',
                             pos_hint={"center_x": 0.5, "center_y": 0.4}
                             )
        self.add_widget(self.greeting)

        # Followup text specifying that the nuid must be at least 9 digits
        self.followup = Label(
                             text="(Must be 9 digits or more)",
                             font_size = 14,
                             color='#474747',
                             pos_hint={"center_x": 0.5, "center_y": 0.35}
                             )
        self.add_widget(self.followup)

        # User Input for entering the NUID
        #   Only accepts numbers
        self.user = TextInput(
                             multiline=False,
                             size=(300, 50),
                             size_hint=(None, None),
                             pos_hint={"center_x": 0.5, "center_y": 0.25},
                             input_filter='int',
                             )
        self.user.bind(text=self.on_text_change)
        self.add_widget(self.user)

        # The login button that takes the user to the next screen.
        #   Appears once a user has typed in at least 9 digits.
        self.button = Button(
                            text="Login",
                            size = (250, 50),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.5, "center_y": 0.15},
                            bold = True,
                            disabled=True,
                            opacity=0,
                            )
        self.button.bind(on_press=self.switch)
        self.add_widget(self.button)

    # The method for switching from this screen to the duo screen.
    #   Called when the user presses the login button.
    def switch(self, item):
        app.screen_manager.transition = NoTransition()
        app.screen_manager.current = 'duo'
    
    # The method for tracking when the user input text changes.
    #   Updates the login button's visibility and functionality when at or below 9 digits typed.
    def on_text_change(self, instance, value):
        if len(self.user.text) < 9:
            self.button.disabled = True
            self.button.opacity = 0
        else:
            self.button.disabled = False
            self.button.opacity = 1





# The Screen Representing a Duo Mobile sign in
#   For now, it displays two images that relate to a mobile sign on, then moves on.
class DuoScreen(FloatLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(CanvasWidget())

         # Right Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.95, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
        # Left Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.05, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))

        # Image
        self.duoimg = Image(
                           source="duoloading.png",
                           size=(500, 500),
                           size_hint=(None, None),
                           pos_hint={"center_x": 0.5, "center_y": 0.5}
                           )
        self.add_widget(self.duoimg)

        # Image
        self.loadingspinner = Image(
                           source="blueloading.gif",
                           size=(64, 64),
                           size_hint=(None, None),
                           pos_hint={"center_x": 0.4725, "center_y": 0.4425},
                           opacity = 1
                           )
        self.add_widget(self.loadingspinner)
    
        # Image
        self.grayspinner = Image(
                           source="grayloading.gif",
                           size=(100, 100),
                           size_hint=(None, None),
                           pos_hint={"center_x": 0.5, "center_y": 0.4},
                           opacity = 0,
                           )
        self.add_widget(self.grayspinner)

        Clock.schedule_interval(self.change_duo_image, 10)
        Clock.schedule_interval(self.schedule_switch, 9)

    def change_duo_image(self, dt):
        if (app.screen_manager.current == 'duo'):
            self.duoimg.source = "duosuccess.png" 
            self.loadingspinner.opacity = 0
            self.grayspinner.opacity = 1
    
    def schedule_switch(self, dt):
        if (self.duoimg.source == "duosuccess.png"):
            app.screen_manager.current = 'events'



class EventGroup(FloatLayout):

    currentselected = "None"

    def __init__(self, title, host, date, time, tags):
        super().__init__()

        self.width = 1000
        self.bind(height = self.setter("height"))
        self.bind(width = self.setter("width"))

        self.outline = Image()
        self.outline.source="roundedsquare.png"
        self.outline.size=(350, 300)
        self.outline.size_hint=(None, None)
        self.outline.pos_hint={"center_x": 0.5, "center_y": 0.5}
        self.outline.allow_stretch = True
        self.outline.keep_ratio = False
        self.add_widget(self.outline)
        
        
        # Title
        self.titlelabel = Label(
                             text=title,
                             font_size = 24,
                             color='#000000',
                             bold=True,
                             pos_hint={"center_x": 0.5, "center_y": 2.5}
                             )
        self.add_widget(self.titlelabel)

        # Host
        self.hostlabel = Label(
                             text="Host: " + host,
                             font_size = 18,
                             color='#000000',
                             bold=False,
                             pos_hint={"center_x": 0.3, "center_y": 2}
                             )
        self.add_widget(self.hostlabel)

        # Date
        self.datelabel = Label(
                             text="Date: " + date,
                             font_size = 18,
                             color='#000000',
                             bold=False,
                             pos_hint={"center_x": 0.3, "center_y": 1.5}
                             )
        self.add_widget(self.datelabel)

        # Time
        self.timelabel = Label(
                             text="Time: " + time,
                             font_size = 18,
                             color='#000000',
                             bold=False,
                             pos_hint={"center_x": 0.3, "center_y": 1}
                             )
        self.add_widget(self.timelabel)

        # Tags
        self.taglabel = Label(
                             text="Tags:            ",
                             font_size = 18,
                             color='#000000',
                             bold=False,
                             pos_hint={"center_x": 0.26, "center_y": 0.5}
                             )
        self.add_widget(self.taglabel)

        # Tags 
        tagtext = ""
        for i in range(3) :
            if i < len(tags):
                tagtext += "\n - " + tags[i]
            else :
                tagtext += "\n - "
        self.tagslabel = Label(
                             text=tagtext,
                             font_size = 18,
                             color='#000000',
                             bold=True,
                             pos_hint={"center_x": 0.3, "center_y": -0.15}
                             )
        self.add_widget(self.tagslabel)

        # The login button that takes the user to the next screen.
        #   Appears once a user has typed in at least 9 digits.
        self.attendbutton = Button(
                            text="4",
                            size = (45, 25),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.35, "center_y": -1.53},
                            bold = True,
                            disabled=False,
                            opacity=1,
                            background_color='#b4ed9a',
                            background_normal=''
                            )
        self.attendbutton.bind(size = self.setter("size"))
        self.attendbutton.bind(on_press=self.attend_click)
        self.add_widget(self.attendbutton)

        # The login button that takes the user to the next screen.
        #   Appears once a user has typed in at least 9 digits.
        self.maybebutton = Button(
                            text="0",
                            size = (45, 25),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.5, "center_y": -1.53},
                            bold = True,
                            disabled=False,
                            opacity=1,
                            background_color='#dbdbdb',
                            background_normal=''
                            )
        #self.button.bind(on_press=self.switch)
        self.add_widget(self.maybebutton)

        # The login button that takes the user to the next screen.
        #   Appears once a user has typed in at least 9 digits.
        self.nobutton = Button(
                            text="3",
                            size = (45, 25),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.65, "center_y": -1.53},
                            bold = True,
                            disabled=False,
                            opacity=1,
                            background_color='#ed8c8c',
                            background_normal=''
                            )
        self.nobutton.bind(on_press=self.no_click)
        self.add_widget(self.nobutton)
    
    def attend_click(self, item):
        if (self.nobutton.size == (45, 35)):
            # Moving the No Button Down
            self.nobutton.text="3"
            self.nobutton.size=(45,25)
            self.nobutton.pos_hint={"center_x": 0.65, "center_y": -1.53}
            self.nobutton.background_color='#ed8c8c'

            # Moving the Yes Button Up
            self.attendbutton.text="5"
            self.attendbutton.size=(45,35)
            self.attendbutton.pos_hint={"center_x": 0.35, "center_y": -1.43}
            self.attendbutton.background_color='#55c95a'

        elif (self.maybebutton.size == (45, 35)):
            # Moving the Maybe Button Down
            self.maybebutton.text="0"
            self.maybebutton.size=(45,25)
            self.maybebutton.pos_hint={"center_x": 0.5, "center_y": -1.53}
            self.maybebutton.background_color='#dbdbdb'

            # Moving the Yes Button Up
            self.attendbutton.text="5"
            self.attendbutton.size=(45,35)
            self.attendbutton.pos_hint={"center_x": 0.35, "center_y": -1.43}
            self.attendbutton.background_color='#55c95a'

        elif (self.attendbutton.size == (45, 35)):
            # Moving the Yes Button Down
            self.attendbutton.text="4"
            self.attendbutton.size=(45,25)
            self.attendbutton.pos_hint={"center_x": 0.35, "center_y": -1.53}
            self.attendbutton.background_color='#b4ed9a'

        else :
            # Moving the Yes Button Up
            self.attendbutton.text="5"
            self.attendbutton.size=(45,35)
            self.attendbutton.pos_hint={"center_x": 0.35, "center_y": -1.43}
            self.attendbutton.background_color='#55c95a'

    def no_click(self, item):
        if (self.nobutton.size == (45, 35)):
            # Moving the No Button Down
            self.nobutton.text="3"
            self.nobutton.size=(45,25)
            self.nobutton.pos_hint={"center_x": 0.65, "center_y": -1.53}
            self.nobutton.background_color='#ed8c8c'

        elif (self.maybebutton.size == (45, 35)):
            # Moving the Maybe Button Down
            self.maybebutton.text="0"
            self.maybebutton.size=(45,25)
            self.maybebutton.pos_hint={"center_x": 0.5, "center_y": -1.53}
            self.maybebutton.background_color='#dbdbdb'

            # Moving the No Button Up
            self.nobutton.text="4"
            self.nobutton.size=(45,35)
            self.nobutton.pos_hint={"center_x": 0.65, "center_y": -1.43}
            self.nobutton.background_color='#c95555'

        elif (self.attendbutton.size == (45, 35)):
            # Moving the Yes Button Down
            self.attendbutton.text="4"
            self.attendbutton.size=(45,25)
            self.attendbutton.pos_hint={"center_x": 0.35, "center_y": -1.53}
            self.attendbutton.background_color='#b4ed9a'

            # Moving the No Button Up
            self.nobutton.text="4"
            self.nobutton.size=(45,35)
            self.nobutton.pos_hint={"center_x": 0.65, "center_y": -1.43}
            self.nobutton.background_color='#c95555'

        else :
            # Moving the No Button Up
            self.nobutton.text="4"
            self.nobutton.size=(45,35)
            self.nobutton.pos_hint={"center_x": 0.65, "center_y": -1.43}
            self.nobutton.background_color='#c95555'
            
        



# The Login Screen
#   This is the first screen that a user will encounter when opening the app
#   Once the user enters their nuid, they can hit the login button to continue to the app
class EventsScreen(FloatLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(CanvasWidget())

        self.window = GridLayout()
        self.window.cols = 1
        self.window.row_force_default = True
        self.window.row_default_height = 50
        #self.window.size_hint_y = None
        self.window.bind(minimum_height = self.window.setter("height"))
        self.window.bind(minimum_width = self.window.setter("width"))
        #self.window.spacing = (10, 10)
        self.window.height = self.window.minimum_height
        self.window.width = self.window.minimum_width
        self.window.width = 700

        self.scrollview = ScrollView()
        self.scrollview.pos_hint = {"center_x": 0.555, "center_y": 0.5}
        self.scrollview.size_hint = (None, 1)
        self.scrollview.width = 500
        self.scrollview.do_scroll_y = True
        self.scrollview.do_scroll_x = False
        self.scrollview.height = self.window.minimum_height
        self.add_widget(self.scrollview)
        self.scrollview.add_widget(self.window)
        
        

        #self.window.cols = 1
        #self.window.size_hint=(1, None)
        self.window.size_hint = (None, None)
        self.window.pos_hint={"center_x": 0.5, "center_y": 0.5}

        # Text title display for the Events Page
        self.attendinglabel = Label(
                             text="You are attending...",
                             font_size = 32,
                             color='#000000',
                             bold=False,
                             underline=True,
                             pos_hint={"center_x": 0.5, "center_y": 0}
                             )

        for i in range(2):
            self.window.add_widget(Label(text=" ", font_size=8))

        self.window.add_widget(self.attendinglabel)

        for i in range(2):
            self.window.add_widget(Label(text=" ", font_size=8))

        self.window.add_widget(EventGroup("Food Court", "RA Alex ", "10/21/24", "6:00 PM ", ["Free Food", "Dinner"]))

        for i in range(5):
            self.window.add_widget(Label(text=" ", font_size=8))

        self.window.add_widget(EventGroup("Rock Climbing", "Ken     ", "10/26/24", "2:00 PM", ["Rock Climbing"]))

        for i in range(30):
            self.window.add_widget(Label(text=" ", font_size=8))

        # Followup text specifying that the nuid must be at least 9 digits
        self.followup = Label(
                             text="(Must be 9 digits or more)",
                             font_size = 14,
                             color='#474747',
                             #pos_hint={"center_x": 0.5, "center_y": 0.35}
                             )
        self.window.add_widget(self.followup)

        # User Input for entering the NUID
        #   Only accepts numbers
        self.user = TextInput(
                             multiline=False,
                             size=(300, 50),
                             size_hint=(None, None),
                             #pos_hint={"center_x": 0.5, "center_y": 0.25},
                             input_filter='int',
                             )
        self.window.add_widget(self.user)

        # The login button that takes the user to the next screen.
        #   Appears once a user has typed in at least 9 digits.
        self.button = Button(
                            text="Login",
                            size = (250, 50),
                            size_hint=(None, None),
                            #pos_hint = {"center_x": 0.5, "center_y": 0.15},
                            bold = True,
                            disabled=False,
                            opacity=1,
                            )
        self.button.bind(on_press=self.switch)
        self.window.add_widget(self.button)

        # Image
        self.add_widget(Image(
                               source="redbar.png",
                               size=(750, 100),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.95},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
         # Image
        self.add_widget(Image(
                               source="redbar.png",
                               size=(750, 100),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.05},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
        # Right Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.95, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
        # Left Border
        self.add_widget(Image(
                               source="blackbar.png",
                               size=(1000, 1500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.05, "center_y": 0.5},
                               allow_stretch = True,
                               keep_ratio = False
                               ))
        
        # Text title display for the Events Page
        self.eventslabel = Label(
                             text="Events",
                             font_size = 48,
                             color='#ffffff',
                             bold=True,
                             pos_hint={"center_x": 0.37, "center_y": 0.95}
                             )
        self.add_widget(self.eventslabel)

        # The Create Event button that opens up the event creation popup
        self.eventbutton = Button(
                            text="+ Create Event",
                            size = (250, 50),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.61, "center_y": 0.95},
                            bold = True,
                            disabled=False,
                            opacity=1,
                            color = '#000000',
                            background_color = '#ffffff',
                            background_normal = ''
                            )
        self.eventbutton.bind(on_press=self.switch)
        self.add_widget(self.eventbutton)

        

    # The method for switching from this screen to the duo screen.
    #   Called when the user presses the login button.
    def switch(self, item):
        app.screen_manager.transition = NoTransition()
        app.screen_manager.current = 'duo'
    
    # The method for tracking when the user input text changes.
    #   Updates the login button's visibility and functionality when at or below 9 digits typed.
    def on_text_change(self, instance, value):
        if len(self.user.text) < 9:
            self.button.disabled = True
            self.button.opacity = 0
        else:
            self.button.disabled = False
            self.button.opacity = 1





# The App that all the Screens will run on.
class ScreenApp(App):
    def build(self):
        self.screen_manager = ScreenManager()        

        self.loginpage = LoginScreen()
        screen = Screen(name='login')
        screen.add_widget(self.loginpage)
        self.screen_manager.add_widget(screen)

        self.duopage = DuoScreen()
        screen = Screen(name='duo')
        screen.add_widget(self.duopage)
        self.screen_manager.add_widget(screen)  

        self.eventspage = EventsScreen()
        screen = Screen(name='events')
        screen.add_widget(self.eventspage)
        self.screen_manager.add_widget(screen)      

        return self.screen_manager

    
app = ScreenApp()
app.run()