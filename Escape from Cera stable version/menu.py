import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# This is a user event that should be sent whenever the game state is changed (at the main game loop level)
EVENT_CHANGE_STATE = pygame.USEREVENT + 1

DESC = [['This is the main menu',
         'Main Menu',
         ''],
        ['Choose a level to load',
         'Load menu',
         ''],
		['Press R to reload a level,'
		 ' Press Esc to exit game',
         'Main objective - Gather all the chests, meet up with other player',
         'Instruction Menu '],
		 ['Choose a level to load',
         'Load menu',
         '']]
TEXT = []
pygame.font.init()
desc_font = pygame.font.Font(None, 24)    # Font to use
for text in DESC:
	tmp = []
	tmp.append(desc_font.render(text[0], True, WHITE))
	tmp.append(desc_font.render(text[1], True, WHITE))
	tmp.append(desc_font.render(text[2], True, WHITE))
	TEXT.append(tmp)
	
class cMenu:

	def __init__(self, x, y, h_pad, v_pad, orientation, number, background,buttonList):
		self.menu_items = []                      # List of menu items
		self.font = pygame.font.Font(None, 32)    # Font to use

		self.x = x                                # Top left corner (of surface)
		self.y = y                                # relative to the screen/window
		self.change_number = number               
		self.orientation = orientation            
		self.horizontal_padding = h_pad           
		self.vertical_padding = v_pad             

		self.selection = 0                        # The currently selected button
		self.u_color = WHITE                      # Color for unselected text
		self.s_color = RED                        # Color for selected text

		self.background = background.copy()       # The unedited background image
		self.draw_surface = background            
		self.centered = False                     # True if the menu is centered
		self.centeredOnScreen = False             # True if the menu is centered

		self.refresh_whole_surface_on_load = False

		self.alignment = {'vertical'  :'top','horizontal':'left'}
		#Add any buttons that were passed in
		self.add_buttons(buttonList)
		self.ret(buttonList)

	def ret(self, buttonList):
		for button in buttonList:
			return button
   # ---redraw_all---------------------------------------------------------
	def redraw_all(self):
		for button in self.menu_items:
			button['redraw'] = True

   # ---[set_refresh_whole_screen_on_load-----------------------------------
	def set_refresh_whole_surface_on_load(self, new_val = True):
		self.refresh_whole_surface_on_load = new_val # Should be True or False

		
   # ---set_font-----------------------------------------------------------
	def set_font(self, font):
		self.font = font

      # We need to update the width and height of the text buttons since we
      # calculated their width and height based on the font
		for button in self.menu_items:
			if button['b_image'] == None:
				width, height = self.font.size(button['text'])
				button['rect'][2] = width
				button['rect'][3] = height

		self.update_buttons = True

   # ---set_alignment------------------------------------------------------
	def set_alignment(self, v_align, h_align):
		if v_align in ['top', 'center', 'bottom']:
			self.alignment['vertical'] = v_align
		if h_align in ['left', 'center', 'right']:
			self.alignment['horizontal'] = h_align
		self.update_buttons = True

   # ---set_center ---------------------------------------------------------
	def set_center(self, centered, centeredOnScreen):
		if centeredOnScreen:
			self.centeredOnScreen = centeredOnScreen
			self.centered = False
		else:
			self.centeredOnScreen = False
			self.centered = centered
		self.update_buttons = True


   # ---add_buttons--------------------------------------------------------
	def add_buttons(self, buttonList):
		for button in buttonList:
			self.menu_items.append(self.create_button(button))
		self.update_buttons = True

   # ---update_button_locations--------------------------------------------
	def update_button_locations(self):
		self.position_buttons()
		self.set_button_images()
		self.update_buttons = False


   # ---create_button------------------------------------------------------
	def create_button(self, button_info):
      # If this button is not an image, set the width and height based on the
      # text
		if button_info[2] == None:
			width, height = self.font.size(button_info[0])
			button_rect = pygame.Rect((0, 0), (width, height))
      # Else this button is a graphic button, so create the width and height
      # based on the image provided
		else:
			width, height = button_info[2].get_size()
			offset = (self.image_highlight_offset, self.image_highlight_offset)
			new_width  = width  + 2 * offset[0]  # Make room for the highlight on
			new_height = height + 2 * offset[1]  # all sides
			button_rect = pygame.Rect((0, 0), (new_width, new_height))

		set_redraw = True     # When the button is created, it needs to be drawn
		set_selected = False  # When the button is created, it is not selected

		new_button = {'text'    : button_info[0],
                    'state'   : button_info[1],
                    'selected': set_selected,
                    'rect'    : button_rect,
                    'offset'  : (0, 0),
                    'redraw'  : set_redraw,
                    'b_image' : button_info[2],  # base image
                    's_image' : None,            # image when selected and not
                    'u_image' : None}            # selected (created in
                                                 # set_button_images)

		return new_button


   # ---set_button_images--------------------------------------------------
	def set_button_images(self):
		for button in self.menu_items:
         # If this button is not an image, create the selected and unselected
         # images based on the text
			if button['b_image'] == None:
				r = self.font.render
				width  = button['rect'][2]
				height = button['rect'][3]
				rect = pygame.Rect(button['offset'], (width, height))

            # For each of the text button (selected and unselected), create a
            # surface of the required size (already calculated before), blit
            # the background image to the surface, then render the text and blit
            # that text onto the same surface.
				selected_image = pygame.Surface((width, height), -1)
				selected_image.blit(self.background, (0, 0), rect)
				text_image   = r(button['text'], True, self.s_color)
				selected_image.blit(text_image, (0, 0))

				unselected_image = pygame.Surface((width, height), -1)
				unselected_image.blit(self.background, (0, 0), rect)
				text_image   = r(button['text'], True, self.u_color)
				unselected_image.blit(text_image, (0, 0))

         # Else this button is a graphic button, so create the selected and
         # unselected images based on the image provided
			else:
				orig_width, orig_height = button['b_image'].get_size()
				new_width  = button['rect'][2]
				new_height = button['rect'][3]
				offset = (self.image_highlight_offset, self.image_highlight_offset)

            # Selected image! --------------------------------------------------
            # Create the surface, fill the surface with the highlight color,
            # then blit the background image to the surface (inside of the
            # highlight area), and then blit the actual button base image over
            # the background
				selected_image = pygame.Surface((new_width, new_height), -1)
				selected_image.fill(self.image_highlight_color)
				rect = pygame.Rect((button['offset'][0] + offset[0],button['offset'][1] + offset[1]),(orig_width, orig_height))
				selected_image.blit(self.background, offset, rect)
				selected_image.blit(button['b_image'], offset)

	            # Unselected image! ------------------------------------------------
	            # Create the surface, blit the background image onto the surface (to
	            # make sure effects go away when the button is no longer selected),
	            # and then blit the actual button base image over the background
				unselected_image = pygame.Surface((new_width, new_height), -1)
				rect = pygame.Rect(button['offset'], (new_width, new_height))
				unselected_image.blit(self.background, (0, 0), rect)
				unselected_image.blit(button['b_image'], offset)

			button['s_image'] = selected_image
			button['u_image'] = unselected_image


   # -- position_buttons---------------------------------------------------
	def position_buttons(self):
		width = 0
		height = 0
		max_width = 0
		max_height = 0
		counter = 0
		x_loc = self.x
		y_loc = self.y

      # Get the maximum width and height of the surfaces
		for button in self.menu_items:
			width  = button['rect'][2]
			height = button['rect'][3]
			max_width = max(width, max_width)
			max_height = max(height, max_height)

      # Position the button in relation to each other
		for button in self.menu_items:
         # Find the offsets for the alignment of the buttons (left, center, or right)
         # Vertical Alignment
			if self.alignment['vertical'] == 'top':
				offset_height = 0
			elif self.alignment['vertical'] == 'center':
				offset_height = (max_height - button['rect'][3])/2
			elif self.alignment['vertical'] == 'bottom':
				offset_height = (max_height - button['rect'][3])
			else:
				offset_height = 0
			
         # Horizontal Alignment
			if self.alignment['horizontal'] == 'left':
				offset_width = 0
			elif self.alignment['horizontal'] == 'center':
				offset_width = (max_width - button['rect'][2])/2
			elif self.alignment['horizontal'] == 'right':
				offset_width = (max_width - button['rect'][2])
			else:
				offset_width = 0
			
         # Move the button location slightly based on the alignment offsets
			x_loc += offset_width
			y_loc += offset_height

         # Assign the location of the button
			button['offset'] = (x_loc, y_loc)

         # Take the alignment offsets away after the button position has been assigned so that the new button can start fresh again
			x_loc -= offset_width
			y_loc -= offset_height

         # Add the width/height to the position based on the orientation of the menu.  Add in the padding.
			if self.orientation == 'vertical':
				y_loc += max_height + self.vertical_padding
			else:
				x_loc += max_width + self.horizontal_padding
			counter += 1

         # If we have reached the self.change_number of buttons, then it is time
         # to start a new row or column
			if counter == self.change_number:
				counter = 0
				if self.orientation == 'vertical':
					x_loc += max_width + self.horizontal_padding
					y_loc = self.y
				else:
					y_loc += max_height + self.vertical_padding
					x_loc = self.x

      # Find the smallest Rect that will contain all of the buttons
		self.contained_rect = self.menu_items[0]['rect'].move(button['offset'])
		for button in self.menu_items:
			temp_rect = button['rect'].move(button['offset'])
			self.contained_rect.union_ip(temp_rect)

      # We shift the buttons around on the screen if they are supposed to be
      # centered (on the surface itself or at (x, y).  We do it here instead of
      # at the beginning of this function becuase we need to know what the
      # self.contained_rect is to know the correct amount to shift them.
		if self.centeredOnScreen:
			shift_x = self.x - (self.draw_surface.get_rect()[2] - self.contained_rect[2]) / 2
			shift_y = self.y - (self.draw_surface.get_rect()[3] - self.contained_rect[3]) / 2
		elif self.centered:
			shift_x = (self.contained_rect[2]) / 2
			shift_y = (self.contained_rect[3]) / 2
		if self.centeredOnScreen or self.centered:
         # Move the buttons to make them centered
			for button in self.menu_items:
				button['offset'] = (button['offset'][0] - shift_x,button['offset'][1] - shift_y)

         # Re-find the smallest Rect that will contain all of the buttons
			self.contained_rect = self.menu_items[0]['rect'].move(button['offset'])
			for button in self.menu_items:
				temp_rect = button['rect'].move(button['offset'])
				self.contained_rect.union_ip(temp_rect)


   # ---update-------------------------------------------------------------
	def update(self, e, c_state):
		redraw_full_menu = False

		self.selection_prev = self.selection
		o = self.orientation
		s = self.selection
		n = self.change_number
		if e.key == pygame.K_DOWN:
			if (o == 'vertical') and ((s + 1) % n != 0):
				self.selection += 1
			elif o == 'horizontal':
				self.selection += n
		elif e.key == pygame.K_UP:
			if (o == 'vertical') and ((s) % n != 0):
				self.selection -= 1
			elif o == 'horizontal':
				self.selection -= n
		elif e.key == pygame.K_RIGHT:
			if o == 'vertical':
				self.selection += n
			elif (o == 'horizontal') and ((s + 1) % n != 0):
				self.selection += 1
		elif e.key == pygame.K_LEFT:
			if o == 'vertical':
				self.selection -= n
			elif (o == 'horizontal') and ((s) % n != 0):
				self.selection -= 1
		elif e.key == pygame.K_RETURN:
			return [None], self.menu_items[s]['state']

		if self.selection >= len(self.menu_items) or self.selection < 0:
			self.selection = self.selection_prev

      # If this is an EVENT_CHANGE_STATE, then this is the first time entered this menu,  set it up
		if e.type == EVENT_CHANGE_STATE:
			self.selection = 0
			self.menu_items[self.selection_prev]['selected'] = False
			self.menu_items[self.selection]['selected'] = True
			self.redraw_all()
			rectangle_list = self.draw_buttons()
			if self.refresh_whole_surface_on_load:
				rectangle_list = pygame.Rect((0, 0), self.draw_surface.get_size())
				return [rectangle_list], c_state
			else:
				return [self.contained_rect], c_state

		elif redraw_full_menu:
			self.menu_items[self.selection_prev]['selected'] = False
			self.menu_items[self.selection]['selected'] = True
			self.redraw_all()
			rectangle_list = self.draw_buttons(original_contained_rect)
			return rectangle_list, c_state

		elif self.selection != self.selection_prev:
			self.menu_items[self.selection_prev]['selected'] = False
			self.menu_items[self.selection]['selected'] = True
			rectangle_list = self.draw_buttons()
			return rectangle_list, c_state

      # If no updates were made, return defaults
		return [None], c_state


   # ---draw_buttons-------------------------------------------------------
	def draw_buttons(self, redraw_rect = None):
		rect_list = []

		if self.update_buttons:
			self.update_button_locations()

      # Cycle through the buttons, only draw the ones that need to be redrawn
		for button in self.menu_items:
			if button['redraw']:
				if button['selected']:
					image = button['s_image']
				else:
					image = button['u_image']

				drawn_rect = self.draw_surface.blit(image,button['offset'],button['rect'])
				rect_list.append(drawn_rect)

		return rect_list
#---EOF-------------------------------------------------------------
