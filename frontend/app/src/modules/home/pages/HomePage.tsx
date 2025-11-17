import { Users, BookOpen, MessageSquare, Calendar, TrendingUp, Plus } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/global/components/ui/card';
import { Button } from '@/global/components/ui/button';
import { Separator } from '@/global/components/ui/separator';

export function HomePage() {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Good evening</h1>
        <p className="text-muted-foreground mt-2 text-lg">
          Welcome back to The Public Square
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">My Clubs</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground mt-1">Active memberships</p>
          </CardContent>
        </Card>

        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Reading List</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground mt-1">Books in progress</p>
          </CardContent>
        </Card>

        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Discussions</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">7</div>
            <p className="text-xs text-muted-foreground mt-1">Unread threads</p>
          </CardContent>
        </Card>

        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Meetings</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground mt-1">This week</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Recent Activity */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Your latest updates and discussions</CardDescription>
              </div>
              <Button variant="ghost" size="sm">View all</Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  action: 'commented on',
                  target: 'Crime and Punishment Discussion',
                  club: 'Classic Literature Club',
                  time: '2 hours ago',
                },
                {
                  action: 'joined',
                  target: 'Philosophy Readers',
                  club: null,
                  time: '1 day ago',
                },
                {
                  action: 'finished reading',
                  target: 'The Brothers Karamazov',
                  club: 'Dostoyevsky Enthusiasts',
                  time: '2 days ago',
                },
              ].map((activity, i) => (
                <div key={i}>
                  <div className="flex items-start gap-4">
                    <div className="flex-1 space-y-1">
                      <p className="text-sm">
                        You <span className="text-muted-foreground">{activity.action}</span>{' '}
                        <span className="font-medium">{activity.target}</span>
                      </p>
                      {activity.club && (
                        <p className="text-xs text-muted-foreground">in {activity.club}</p>
                      )}
                      <p className="text-xs text-muted-foreground">{activity.time}</p>
                    </div>
                  </div>
                  {i < 2 && <Separator className="mt-4" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Meetings */}
        <Card>
          <CardHeader>
            <CardTitle>Upcoming Meetings</CardTitle>
            <CardDescription>Your scheduled book club sessions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  title: 'Weekly Discussion',
                  club: 'Classic Literature',
                  date: 'Tomorrow',
                  time: '7:00 PM',
                },
                {
                  title: 'Chapter Review',
                  club: 'Modern Fiction',
                  date: 'Friday',
                  time: '6:30 PM',
                },
              ].map((meeting, i) => (
                <div key={i}>
                  <div className="flex items-start justify-between gap-2">
                    <div className="space-y-1">
                      <p className="text-sm font-medium leading-none">{meeting.title}</p>
                      <p className="text-xs text-muted-foreground">{meeting.club}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs font-medium">{meeting.date}</p>
                      <p className="text-xs text-muted-foreground">{meeting.time}</p>
                    </div>
                  </div>
                  {i < 1 && <Separator className="mt-4" />}
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4" size="sm">
              <Calendar className="mr-2 h-4 w-4" />
              View Calendar
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Trending Discussions */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-accent" />
                Trending Discussions
              </CardTitle>
              <CardDescription>Popular topics across The Public Square</CardDescription>
            </div>
            <Button variant="ghost" size="sm">See more</Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                title: 'Existentialism in Modern Literature',
                page: 'Philosophy',
                replies: 45,
                participants: 12,
              },
              {
                title: 'The Ethics of Dostoyevsky',
                page: 'Theology',
                replies: 32,
                participants: 8,
              },
              {
                title: 'Reading Strategies for Dense Texts',
                page: 'Book Discussion',
                replies: 28,
                participants: 15,
              },
            ].map((discussion, i) => (
              <Card key={i} className="hover:bg-accent/30 transition-colors cursor-pointer">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium line-clamp-2">
                    {discussion.title}
                  </CardTitle>
                  <CardDescription className="text-xs">{discussion.page}</CardDescription>
                </CardHeader>
                <CardContent className="pb-3">
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>{discussion.replies} replies</span>
                    <span>•</span>
                    <span>{discussion.participants} participants</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Start Actions */}
      <Card className="border-accent/50">
        <CardHeader>
          <CardTitle>Get Started</CardTitle>
          <CardDescription>
            New to The Public Square? Here are some ways to begin your journey
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="justify-start h-auto py-3">
              <Plus className="mr-2 h-4 w-4" />
              <div className="text-left">
                <div className="font-medium">Join a Club</div>
                <div className="text-xs text-muted-foreground">Find your community</div>
              </div>
            </Button>
            <Button variant="outline" className="justify-start h-auto py-3">
              <Plus className="mr-2 h-4 w-4" />
              <div className="text-left">
                <div className="font-medium">Add a Book</div>
                <div className="text-xs text-muted-foreground">Build your library</div>
              </div>
            </Button>
            <Button variant="outline" className="justify-start h-auto py-3">
              <Plus className="mr-2 h-4 w-4" />
              <div className="text-left">
                <div className="font-medium">Start Discussion</div>
                <div className="text-xs text-muted-foreground">Share your thoughts</div>
              </div>
            </Button>
            <Button variant="outline" className="justify-start h-auto py-3">
              <Plus className="mr-2 h-4 w-4" />
              <div className="text-left">
                <div className="font-medium">Create Club</div>
                <div className="text-xs text-muted-foreground">Lead a community</div>
              </div>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
