#from django.conf import settings
from .server_tools import create_session_on_server
#from .management.commands.create_session import create_pre_authenticated_session
from .base import FunctionalTest
from .home_and_list_pages import HomePage

class MyListsTest(FunctionalTest):

	def test_logged_in_users_lists_are_save_as_my_lists(self):
		# Edith is a logged-in user
		self.create_pre_authenticated_session('edith@example.com')

		# She goes to the home page and starts a MyListsTest
		self.browser.get(self.server_url)
		list_page = HomePage(self).start_new_list('Reticulate splines')
		list_page.add_new_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		# She notices a "My lists" link, for the first time.
		HomePage(self).go_to_my_lists_page()

		#She sees that her list is in there, named  according to its
		# first list item
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)

		# She decides to start another list, just to see
		self.browser.get(self.server_url)
		#self.get_item_input_box().send_keys('Click cows\n')
		list_page2 = HomePage(self).start_new_list('Click cows')
		second_list_url = self.browser.current_url

		# Under "my lists", her new list appears
		self.browser.find_element_by_link_text('My lists').click()
		self.browser.find_element_by_link_text('Click cows').click()
		self.assertEqual(self.browser.current_url, second_list_url)

		# She logs out. The "My lists" option disappears
		self.browser.find_element_by_id('id_logout').click()
		self.assertEqual(
			self.browser.find_elements_by_link_text('My lists'),
			[]
		)
