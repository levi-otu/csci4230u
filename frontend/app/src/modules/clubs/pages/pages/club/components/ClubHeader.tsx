/**
 * ClubHeader Component
 * Displays club header with name, topic, and action buttons
 */

import React from 'react';
import { ArrowLeft, Users, Tag, UserPlus, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/global/components/ui/button';
import { Badge } from '@/global/components/ui/badge';
import type { Club } from '@/global/models/club.models';

export interface ClubHeaderProps {
  club: Club;
  isUserMember: boolean;
  memberCount?: number;
  onJoinClick?: () => void;
  onLeaveClick?: () => void;
  isJoining?: boolean;
  isLeaving?: boolean;
}

/**
 * ClubHeader component for club detail page
 */
export const ClubHeader: React.FC<ClubHeaderProps> = ({
  club,
  isUserMember,
  memberCount = 0,
  onJoinClick,
  onLeaveClick,
  isJoining = false,
  isLeaving = false,
}) => {
  const navigate = useNavigate();

  return (
    <div className="border-b bg-card">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        {/* Back Button */}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate('/clubs')}
          className="mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Clubs
        </Button>

        {/* Header Content */}
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold">{club.name}</h1>
              {!club.is_active && (
                <Badge variant="destructive">Inactive</Badge>
              )}
            </div>

            {club.description && (
              <p className="text-muted-foreground text-lg mb-4">
                {club.description}
              </p>
            )}

            <div className="flex items-center gap-4 flex-wrap">
              {club.topic && (
                <div className="flex items-center gap-1.5 text-sm">
                  <Tag className="h-4 w-4 text-muted-foreground" />
                  <Badge variant="secondary">{club.topic}</Badge>
                </div>
              )}

              <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <Users className="h-4 w-4" />
                <span>{memberCount} member{memberCount !== 1 ? 's' : ''}</span>
                {club.max_members && (
                  <span className="text-muted-foreground">
                    / {club.max_members} max
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            {isUserMember ? (
              <Button
                variant="outline"
                onClick={onLeaveClick}
                disabled={isLeaving}
              >
                <LogOut className="h-4 w-4 mr-2" />
                {isLeaving ? 'Leaving...' : 'Leave Club'}
              </Button>
            ) : (
              <Button
                onClick={onJoinClick}
                disabled={isJoining || !club.is_active}
              >
                <UserPlus className="h-4 w-4 mr-2" />
                {isJoining ? 'Joining...' : 'Join Club'}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClubHeader;
