import unittest 
import main

from flask import session

class Testing(unittest.TestCase):
  def setUp(self):
    self.app = main.app.test_client()

  def test_root(self):
    out = self.app.get('/')
    assert '200 OK' in out.status
    assert 'charset=utf-8' in out.content_type
    assert 'text/html' in out.content_type

  def test_logout_updates_sessions_and_redirects(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['logged_in'] = True
        sess['admin'] = True

      out = c.get('/logout')
      assert main.session['logged_in'] is False  
      assert main.session['admin'] is False
      assert '302 FOUND' in out.status
   
  def test_admin_editor_redirects_when_not_admin(self):
    out = self.app.get('/admin_editor/')
    assert '302 FOUND' in out.status

  def test_admin_editor_succes_with_admin(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['admin'] = True
      out = c.get('/admin_editor/')
      assert '200 OK' in out.status
      assert 'charset=utf-8' in out.content_type
      assert 'text/html' in out.content_type

  def test_view_bookings_when_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['logged_in'] = True
        user = {}
        user['username'] = "test"
        user['user_id'] = 1
        sess['user'] = user

      out = c.get('/rossa/mybookings')
      assert '200 OK' in out.status
      assert 'charset=utf-8' in out.content_type
      assert 'text/html' in out.content_type

  def test_view_bookings_when_not_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['logged_in'] = False

      out = c.get('/test/mybookings')
      assert '302 FOUND' in out.status
  
  def test_get_colony_ads_index(self):
    out = self.app.get('/colony_ads/mars/')
    assert '200 OK' in out.status
    assert 'charset=utf-8' in out.content_type
    assert 'text/html' in out.content_type

  def test_colony_chat_redirect_when_not_logged_in(self):
    out = self.app.get('/colony_chat') 
    assert '302 FOUND' in out.status

  def test_colony_chat_ok_when_logged_in(self): 
    with self.app as c:
      with c.session_transaction() as sess:
        sess['logged_in'] = True
        user = {}
        user['username'] = "test"
        sess['user'] = user

      out = c.get('/colony_chat')
      assert '200 OK' in out.status
      assert 'charset=utf-8' in out.content_type
      assert 'text/html' in out.content_type
  
  def test_404(self):
    out = self.app.get('/nonsense/')
    
    assert '404 NOT FOUND' in out.status
    assert 'charset=utf-8' in out.content_type
    assert 'text/html' in out.content_type

if __name__ == "__main__":
  unittest.main()
