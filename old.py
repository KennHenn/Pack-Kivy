class BasicApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.3, 1)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Image
        self.window.add_widget(Image(source="pack.png"))

        # Text
        self.greeting = Label(
                             text="Please Enter your NUID Below",
                             font_size = 18
                             )
        self.window.add_widget(self.greeting)

        # User Input
        self.user = TextInput(
                             multiline=False,
                             size_hint = (0.8, 0.2)
                             )
        self.window.add_widget(self.user)

        # Button
        self.button = Button(
                            text="Login",
                            size_hint = (0.8, 0.2),
                            bold = True,
                            )
        self.button.bind(on_press=self.buttonpressed)
        self.window.add_widget(self.button)

        # Return!
        return self.window
    
    def buttonpressed(self, instance):
        self.greeting.text = "Oh right, you're " + self.user.text + ". My fault."


class FloatApp(App):
    def build(self):
        self.window = FloatLayout()
        self.window.add_widget(CanvasWidget())

        # Image
        self.window.add_widget(Image(
                               source="pack.png",
                               size=(500, 500),
                               size_hint=(None, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.85}
                               ))

        # # Text
        self.greeting = Label(
                             text="Please Enter your NUID Below",
                             font_size = 18,
                             color='#000000',
                             pos_hint={"center_x": 0.5, "center_y": 0.4}
                             )
        self.window.add_widget(self.greeting)

        self.followup = Label(
                             text="(Must be 9 numbers or more)",
                             font_size = 14,
                             color='#474747',
                             pos_hint={"center_x": 0.5, "center_y": 0.35}
                             )
        self.window.add_widget(self.followup)

        # User Input
        self.user = TextInput(
                             multiline=False,
                             size=(300, 50),
                             size_hint=(None, None),
                             pos_hint={"center_x": 0.5, "center_y": 0.25},
                             input_filter='int',
                             )
        self.user.bind(text=self.on_text_change)
        self.window.add_widget(self.user)


        # Button
        self.button = Button(
                            text="Login",
                            size = (250, 50),
                            size_hint=(None, None),
                            pos_hint = {"center_x": 0.5, "center_y": 0.15},
                            bold = True,
                            disabled=True,
                            opacity=0,
                            )
        self.button.bind(on_press=self.buttonpressed)
        self.window.add_widget(self.button)

        

        # Return!
        return self.window
    
    def buttonpressed(self, instance):
        self.greeting.text = "Oh right, you're " + self.user.text + ". My fault."
    
    def on_text_change(self, instance, value):
        if len(self.user.text) < 9:
            self.button.disabled = True
            self.button.opacity = 0
        else:
            self.button.disabled = False
            self.button.opacity = 1