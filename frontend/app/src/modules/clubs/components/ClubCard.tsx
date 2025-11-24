/**
 * ClubCard Component
 * Displays a club in a card format with join/view actions
 */

import React from 'react';
import { Users, Calendar, Tag } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import { Button } from '@/global/components/ui/button';
import { Badge } from '@/global/components/ui/badge';
import type { Club } from '@/global/models/club.models';

export interface ClubCardProps {
  club: Club;
  isUserMember?: boolean;
  onJoinClick?: (clubId: string) => void;
  onViewClick?: (clubId: string) => void;
  isJoining?: boolean;
}

/**
 * ClubCard component for displaying individual club information
 */
export const ClubCard: React.FC<ClubCardProps> = ({
  club,
  isUserMember = false,
  onJoinClick,
  onViewClick,
  isJoining = false,
}) => {
  // Format date to readable string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <Card className="h-full flex flex-col hover:shadow-lg transition-shadow duration-200">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <CardTitle className="text-xl font-bold line-clamp-1">
              {club.name}
            </CardTitle>
            {club.topic && (
              <div className="flex items-center gap-1 mt-2">
                <Tag className="h-3 w-3 text-muted-foreground" />
                <Badge variant="secondary" className="text-xs">
                  {club.topic}
                </Badge>
              </div>
            )}
          </div>
          {!club.is_active && (
            <Badge variant="destructive" className="text-xs">
              Inactive
            </Badge>
          )}
        </div>
        {club.description && (
          <CardDescription className="line-clamp-2 mt-2">
            {club.description}
          </CardDescription>
        )}
      </CardHeader>

      <CardContent className="flex-1">
        <div className="flex flex-col gap-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            <span>Created {formatDate(club.created_at)}</span>
          </div>
          {club.max_members && (
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>Max {club.max_members} members</span>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="flex gap-2">
        {isUserMember ? (
          <Button
            onClick={() => onViewClick?.(club.id)}
            className="flex-1"
            variant="default"
          >
            View Club
          </Button>
        ) : (
          <>
            <Button
              onClick={() => onViewClick?.(club.id)}
              className="flex-1"
              variant="outline"
            >
              View Details
            </Button>
            <Button
              onClick={() => onJoinClick?.(club.id)}
              className="flex-1"
              disabled={isJoining || !club.is_active}
            >
              {isJoining ? 'Joining...' : 'Join Club'}
            </Button>
          </>
        )}
      </CardFooter>
    </Card>
  );
};

export default ClubCard;
