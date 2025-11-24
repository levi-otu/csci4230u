/**
 * Clubs Page
 * Main page for discovering and managing book clubs
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, BookOpen, Users } from 'lucide-react';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
import { useAppSelector } from '@/global/hooks/useAppSelector';
import {
  fetchAllClubsAsync,
  fetchUserClubsAsync,
  createClubAsync,
  joinClubAsync,
} from '@/global/store/slices';
import { Button } from '@/global/components/ui/button';
import { Separator } from '@/global/components/ui/separator';
import { ClubCard } from '../components/ClubCard';
import { CreateClubModal } from '../components/CreateClubModal';
import type { CreateClubRequest } from '@/global/models/club.models';

/**
 * Clubs Page Component
 */
export const Clubs: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { allClubs, userClubs, isLoading, isCreating, isJoining } =
    useAppSelector((state) => state.clubs);
  const { user } = useAppSelector((state) => state.auth);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'discover' | 'my-clubs'>('discover');
  const [joiningClubId, setJoiningClubId] = useState<string | null>(null);

  // Fetch clubs on mount
  useEffect(() => {
    dispatch(fetchAllClubsAsync({ skip: 0, limit: 100 }));
    if (user?.id) {
      dispatch(fetchUserClubsAsync(user.id));
    }
  }, [dispatch, user?.id]);

  // Handle create club
  const handleCreateClub = async (clubData: CreateClubRequest) => {
    const result = await dispatch(createClubAsync(clubData));
    if (createClubAsync.fulfilled.match(result)) {
      setIsCreateModalOpen(false);
      // Optionally show success message
    }
  };

  // Handle join club
  const handleJoinClub = async (clubId: string) => {
    if (!user?.id) return;

    setJoiningClubId(clubId);
    const result = await dispatch(
      joinClubAsync({
        clubId,
        membershipData: { user_id: user.id, role: 'member' },
      })
    );

    if (joinClubAsync.fulfilled.match(result)) {
      // Optionally show success message
      // Refresh user clubs
      dispatch(fetchUserClubsAsync(user.id));
    }
    setJoiningClubId(null);
  };

  // Handle view club
  const handleViewClub = (clubId: string) => {
    // Navigate to club detail page
    navigate(`/clubs/${clubId}`);
  };

  // Check if user is member of a club
  const isUserMember = (clubId: string): boolean => {
    return userClubs.some((club) => club.id === clubId);
  };

  // Get clubs to display based on active tab
  const displayedClubs = activeTab === 'my-clubs' ? userClubs : allClubs;

  // Filter out user's clubs from discover tab
  const discoverClubs =
    activeTab === 'discover'
      ? allClubs.filter((club) => !isUserMember(club.id))
      : allClubs;

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <div className="flex flex-col gap-4 mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <BookOpen className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Book Clubs</h1>
              <p className="text-muted-foreground">
                Discover and join book clubs that match your interests
              </p>
            </div>
          </div>
          <Button onClick={() => setIsCreateModalOpen(true)} size="lg">
            <Plus className="h-4 w-4 mr-2" />
            Create Club
          </Button>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-4 border-b">
          <button
            onClick={() => setActiveTab('discover')}
            className={`pb-3 px-2 font-medium transition-colors relative cursor-pointer ${
              activeTab === 'discover'
                ? 'text-primary'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>Discover Clubs</span>
            </div>
            {activeTab === 'discover' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />
            )}
          </button>
          <button
            onClick={() => setActiveTab('my-clubs')}
            className={`pb-3 px-2 font-medium transition-colors relative cursor-pointer ${
              activeTab === 'my-clubs'
                ? 'text-primary'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" />
              <span>My Clubs</span>
              {userClubs.length > 0 && (
                <span className="ml-1 px-2 py-0.5 text-xs bg-primary/10 text-primary rounded-full">
                  {userClubs.length}
                </span>
              )}
            </div>
            {activeTab === 'my-clubs' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />
            )}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
              <p className="text-sm text-muted-foreground">Loading clubs...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Empty State */}
            {displayedClubs.length === 0 && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="p-4 bg-muted rounded-full mb-4">
                  {activeTab === 'my-clubs' ? (
                    <BookOpen className="h-8 w-8 text-muted-foreground" />
                  ) : (
                    <Users className="h-8 w-8 text-muted-foreground" />
                  )}
                </div>
                <h3 className="text-lg font-semibold mb-2">
                  {activeTab === 'my-clubs'
                    ? "You haven't joined any clubs yet"
                    : 'No clubs available'}
                </h3>
                <p className="text-muted-foreground mb-4 max-w-md">
                  {activeTab === 'my-clubs'
                    ? 'Discover clubs and join ones that interest you, or create your own!'
                    : 'Be the first to create a book club and start building your community.'}
                </p>
                {activeTab === 'my-clubs' && (
                  <Button onClick={() => setActiveTab('discover')}>
                    Discover Clubs
                  </Button>
                )}
              </div>
            )}

            {/* Clubs Grid */}
            {displayedClubs.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {(activeTab === 'discover' ? discoverClubs : displayedClubs).map(
                  (club) => (
                    <ClubCard
                      key={club.id}
                      club={club}
                      isUserMember={isUserMember(club.id)}
                      onJoinClick={handleJoinClub}
                      onViewClick={handleViewClub}
                      isJoining={joiningClubId === club.id}
                    />
                  )
                )}
              </div>
            )}
          </>
        )}
      </div>

      {/* Create Club Modal */}
      <CreateClubModal
        open={isCreateModalOpen}
        onOpenChange={setIsCreateModalOpen}
        onSubmit={handleCreateClub}
        isCreating={isCreating}
      />
    </div>
  );
};

export default Clubs;
