/**
 * Club Detail Page
 * Displays detailed information about a specific club
 */

import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
import { useAppSelector } from '@/global/hooks/useAppSelector';
import {
  fetchClubByIdAsync,
  joinClubAsync,
  leaveClubAsync,
  fetchUserClubsAsync,
} from '@/global/store/slices';
import JoinClubService from '@/global/api/actions/clubs/api-join-club.service';
import { ClubHeader } from './components/ClubHeader';
import { ClubOverview } from './components/ClubOverview';
import { CurrentBook } from './components/CurrentBook';
import { NextMeeting } from './components/NextMeeting';
import { ClubDiscussions } from './components/ClubDiscussions';
import { ClubMembers } from './components/ClubMembers';
import type { CurrentBookData } from './components/CurrentBook';
import type { NextMeetingData } from './components/NextMeeting';
import type { Discussion } from './components/ClubDiscussions';
import type { Member } from './components/ClubMembers';

/**
 * Club Detail Page Component
 */
export const Club: React.FC = () => {
  const { clubId } = useParams<{ clubId: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const { selectedClub, isLoading, isJoining } = useAppSelector(
    (state) => state.clubs
  );
  const { user } = useAppSelector((state) => state.auth);

  const [isUserMember, setIsUserMember] = useState(false);
  const [clubMembers, setClubMembers] = useState<Member[]>([]);
  const [isFetchingMembers, setIsFetchingMembers] = useState(false);

  // Fetch club data on mount
  useEffect(() => {
    if (clubId) {
      dispatch(fetchClubByIdAsync(clubId));
    }
  }, [dispatch, clubId]);

  // Fetch club members helper
  const fetchMembers = async () => {
    if (!clubId) return;

    setIsFetchingMembers(true);
    try {
      const memberships = await JoinClubService.getClubMembers(clubId);
      // Convert UserClubMembership to Member format
      const members: Member[] = memberships.map((membership) => ({
        userId: membership.user_id,
        username: membership.username || membership.user_id,
        fullName: membership.full_name || null,
        email: membership.email || undefined,
        role: membership.role as 'owner' | 'member',
        joinDate: membership.join_date,
      }));
      setClubMembers(members);
    } catch (error) {
      console.error('Failed to fetch club members:', error);
    } finally {
      setIsFetchingMembers(false);
    }
  };

  // Fetch club members on mount
  useEffect(() => {
    fetchMembers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clubId]);

  // Check if user is a member
  useEffect(() => {
    if (user?.id && selectedClub) {
      // TODO: Implement proper membership check via API
      // For now, fetch user clubs and check if this club is in the list
      dispatch(fetchUserClubsAsync(user.id)).then((result) => {
        if (fetchUserClubsAsync.fulfilled.match(result)) {
          const isMember = result.payload.some(
            (club) => club.id === selectedClub.id
          );
          setIsUserMember(isMember);
        }
      });
    }
  }, [dispatch, user?.id, selectedClub]);

  // Handle join club
  const handleJoinClub = async () => {
    if (!user?.id || !clubId) return;

    const result = await dispatch(
      joinClubAsync({
        clubId,
        membershipData: { user_id: user.id, role: 'member' },
      })
    );

    if (joinClubAsync.fulfilled.match(result)) {
      setIsUserMember(true);
      // Refresh club data to get updated member count
      dispatch(fetchClubByIdAsync(clubId));
      // Refresh members list
      await fetchMembers();
    }
  };

  // Handle leave club
  const handleLeaveClub = async () => {
    if (!user?.id || !clubId) return;

    const result = await dispatch(
      leaveClubAsync({
        clubId,
        userId: user.id,
      })
    );

    if (leaveClubAsync.fulfilled.match(result)) {
      setIsUserMember(false);
      // Refresh club data to get updated member count
      dispatch(fetchClubByIdAsync(clubId));
      // Refresh members list
      await fetchMembers();
      // Optionally navigate back to clubs page
      navigate('/clubs');
    }
  };

  // Handle discussion click
  const handleDiscussionClick = (discussionId: string) => {
    // TODO: Navigate to discussion detail page
    console.log('Navigate to discussion:', discussionId);
  };

  // Handle new discussion click
  const handleNewDiscussionClick = () => {
    // TODO: Open new discussion modal
    console.log('Open new discussion modal');
  };

  // Mock data for demonstration - TODO: Replace with real API data
  const currentBook: CurrentBookData | null = selectedClub
    ? {
        title: 'The Great Gatsby',
        author: 'F. Scott Fitzgerald',
        coverUrl: 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
        startDate: '2025-01-15',
        endDate: '2025-02-15',
        progress: 45,
        currentChapter: '5',
        totalChapters: 9,
      }
    : null;

  const nextMeeting: NextMeetingData | null = selectedClub
    ? {
        id: '1',
        title: 'Chapter Discussion: The Green Light',
        date: '2025-01-28',
        time: '7:00 PM EST',
        duration: 90,
        isVirtual: true,
        meetingLink: 'https://meet.example.com/club-meeting',
        chapters: ['Chapter 5', 'Chapter 6'],
        agenda:
          'Discuss the symbolism of the green light and its significance in the story. Analyze the character development of Gatsby and Daisy.',
        description: 'Join us for an engaging discussion about the pivotal chapters',
      }
    : null;

  const discussions: Discussion[] = selectedClub
    ? [
        {
          id: '1',
          title: 'What do you think about Gatsby\'s character?',
          author: {
            id: '1',
            username: 'bookworm123',
          },
          createdAt: '2025-01-20T10:00:00Z',
          lastActivityAt: '2025-01-22T15:30:00Z',
          replyCount: 12,
          excerpt:
            'I find Gatsby to be such a complex character. His dedication is both admirable and tragic...',
          tags: ['character-analysis'],
          isPinned: true,
        },
        {
          id: '2',
          title: 'The symbolism of colors in the novel',
          author: {
            id: '2',
            username: 'literaryfan',
          },
          createdAt: '2025-01-21T14:00:00Z',
          lastActivityAt: '2025-01-21T16:45:00Z',
          replyCount: 8,
          excerpt: 'Has anyone noticed how Fitzgerald uses colors throughout?',
          tags: ['symbolism', 'analysis'],
        },
      ]
    : [];

  // Loading state
  if (isLoading && !selectedClub) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="flex items-center justify-center py-12">
          <div className="text-center space-y-2">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
            <p className="text-sm text-muted-foreground">Loading club...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (!selectedClub && !isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <h3 className="text-lg font-semibold mb-2">Club not found</h3>
          <p className="text-muted-foreground mb-4">
            The club you're looking for doesn't exist or has been removed.
          </p>
          <button
            onClick={() => navigate('/clubs')}
            className="text-primary hover:underline"
          >
            Back to Clubs
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {selectedClub && (
        <div className="space-y-6">
          {/* Header */}
          <ClubHeader
            club={selectedClub}
            isUserMember={isUserMember}
            memberCount={clubMembers.length}
            onJoinClick={handleJoinClub}
            onLeaveClick={handleLeaveClub}
            isJoining={isJoining}
          />

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Content - 2 columns */}
            <div className="lg:col-span-2 space-y-6">
              <ClubOverview
                club={selectedClub}
                memberCount={clubMembers.length}
                totalDiscussions={discussions.length}
                totalMeetings={1}
              />

              <CurrentBook book={currentBook} />

              <NextMeeting meeting={nextMeeting} />

              <ClubDiscussions
                discussions={discussions}
                onDiscussionClick={handleDiscussionClick}
                onNewDiscussionClick={
                  isUserMember ? handleNewDiscussionClick : undefined
                }
              />
            </div>

            {/* Sidebar - 1 column */}
            <div className="lg:col-span-1">
              <ClubMembers
                members={clubMembers}
                currentUserId={user?.id}
                isLoading={isFetchingMembers}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Club;
