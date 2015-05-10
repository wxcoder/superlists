from selenium import webdriver
from .base import FunctionalTest
from .home_and_list_pages import HomePage

def quit_if_possible(browser):
	try: browser.quit()
	except: pass

class SharingTest(FunctionalTest):
	# Edith is a logged-in user
	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		self.create_pre_authenticated_session('edith@example.com')
		edith_browser = self.browser
		self.addCleanup(lambda: quit_if_possible(edith_browser))

		# Her friend Oniciferous is also hanging out on the lists site
		oni_browser = webdriver.Firefox()
		self.addCleanup(lambda: quit_if_possible(oni_browser))
		self.browser = oni_browser
		self.create_pre_authenticated_session('oniciferous@example.com')

		# Edith goes to the home page and starts a list
		self.browser = edith_browser
		list_page = HomePage(self).start_new_list('Get help')

		# She notices a "Share this list" option
		share_box = list_page.get_share_box()
		self.assertEqual(
			share_box.get_attribute('placeholder'),
			'your-friend@example.com'
		)

		# She shares her list.
		# The pages updates to say that it's shared with Oniciferous:
		list_page.share_list_with('oniciferous@example.com')

		# Oniciferous now goes to the lists page with his browser
		self.browser = oni_browser
		HomePage(self).go_to_home_page().go_to_my_lists_page()

		# He sees Edith's list in there!
		self.browser.find_element_by_link_text('Get help').click()
		