from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  #To make SQLAlchemy to use an in-memory SQLite db during the tests rather than regular db
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




    def test_password_hashing(self):
        u = User(username = 'shahid')
        u.set_password('test123')
        self.assertFalse(u.check_password('123test'))
        self.assertTrue(u.check_password('test123'))

    def test_avatar(self):
        u = User(username = 'Shahid ul Islam', email= 'shahid.bhat1994@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         '43ffa62f1995b7ea21252a1ae95fc799'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='shahid', email='shahid.bhat1994@gmail.com')
        u2 = User(username='shahid222', email='shahid.bhat1994@ymail.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'shahid222')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'shahid')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):

        u1 = User(username='shahid', email='shahid.bhat1994@gmail.com')
        u2 = User(username='shahid222', email='shahid.bhat1994@ymail.com')
        u3 = User(username='shahid333', email='shahid@codemantra.in')
        u4 = User(username='shahid444', email='shahid@hotmail.in')

        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from shahid", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from shahid222", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from shahid333", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from shahid444", author=u4,
                  timestamp=now + timedelta(seconds=2))

        db.session.add_all([p1, p2, p3, p4])

        db.session.commit()

        # setup the followers
        u1.follow(u2)  # shahid follows shahid222
        u1.follow(u4)  # shahid follows shahid444
        u2.follow(u3)  # shahid222 follows shahid333
        u3.follow(u4)  # shahid333 follows shahid444

        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)

