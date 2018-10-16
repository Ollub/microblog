from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def seyUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@qxample.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        sb.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u2.folowers.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Susan')
        self.assertEqual(u2.followers.first().username, 'John')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        #create users
        u1 = User(username='Oleg', email='orlov.o@mail.ru')
        u2 = User(username='Jane', email='kurilova@mail.ru')
        u3 = User(username='Brad', email='holli@wood.com')
        u4 = User(username='Pit', email='bolly@wood.com')
        db.session.add_all([u1, u2, u3, u4])

        #create posts
        now = datetime.utcnow()
        p1 = Post(body='post from Oleg', author=u1, 
                timestamp=now + timedelta(seconds=1))
        p2 = Post(body='post from Jane', author=u2, 
                timestamp=now + timedelta(seconds=4))
        p3 = Post(body='post from Brad', author=u3, 
                timestamp=now + timedelta(seconds=3))
        p4 = Post(body='post from Pit', author=u4, 
                timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2) #Oleg follows Jane
        u1.follow(u4) #Oleg follows Pit
        u2.follow(u3) #Jane follows Brad
        u3.follow(u4) #Brad follows Pit
        db.session.commit()

        # checked the followed posts of each user
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




