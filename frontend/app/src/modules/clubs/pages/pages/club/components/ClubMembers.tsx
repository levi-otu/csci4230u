/**
 * ClubMembers Component
 * Displays list of club members
 */

import React from 'react';
import { Users, User, Crown, Calendar } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import { Badge } from '@/global/components/ui/badge';

export interface Member {
  userId: string;
  username: string;
  fullName?: string | null;
  email?: string;
  avatarUrl?: string;
  role: 'owner' | 'member';
  joinDate: string;
}

export interface ClubMembersProps {
  members: Member[];
  currentUserId?: string;
  isLoading?: boolean;
}

/**
 * ClubMembers component
 */
export const ClubMembers: React.FC<ClubMembersProps> = ({
  members,
  currentUserId,
  isLoading = false,
}) => {
  // Format date to readable string
  const formatJoinDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    });
  };

  // Sort members: owners first, then by join date
  const sortedMembers = [...members].sort((a, b) => {
    if (a.role === 'owner' && b.role !== 'owner') return -1;
    if (a.role !== 'owner' && b.role === 'owner') return 1;
    return new Date(a.joinDate).getTime() - new Date(b.joinDate).getTime();
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle>Members</CardTitle>
        <CardDescription>
          {members.length} {members.length === 1 ? 'member' : 'members'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-center space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
              <p className="text-sm text-muted-foreground">Loading members...</p>
            </div>
          </div>
        ) : members.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="p-4 bg-muted rounded-full mb-4">
              <Users className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm text-muted-foreground">
              No members yet
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {sortedMembers.map((member) => (
              <div
                key={member.userId}
                className={`flex items-center gap-3 p-3 rounded-lg border ${
                  member.userId === currentUserId
                    ? 'bg-primary/5 border-primary/20'
                    : 'hover:bg-muted/50'
                } transition-colors`}
              >
                {/* Avatar */}
                <div className="flex-shrink-0">
                  {member.avatarUrl ? (
                    <img
                      src={member.avatarUrl}
                      alt={member.username}
                      className="w-10 h-10 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
                      <User className="h-5 w-5 text-muted-foreground" />
                    </div>
                  )}
                </div>

                {/* Member Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-medium text-sm truncate">
                      {member.fullName || member.username}
                    </p>
                    {member.userId === currentUserId && (
                      <Badge variant="outline" className="text-xs">
                        You
                      </Badge>
                    )}
                  </div>
                  {member.fullName && (
                    <p className="text-xs text-muted-foreground truncate">
                      @{member.username}
                    </p>
                  )}
                  <div className="flex items-center gap-1 mt-1">
                    <Calendar className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">
                      Joined {formatJoinDate(member.joinDate)}
                    </span>
                  </div>
                </div>

                {/* Role Badge */}
                <div className="flex-shrink-0">
                  {member.role === 'owner' ? (
                    <Badge variant="default" className="flex items-center gap-1">
                      <Crown className="h-3 w-3" />
                      Owner
                    </Badge>
                  ) : (
                    <Badge variant="secondary">Member</Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ClubMembers;
