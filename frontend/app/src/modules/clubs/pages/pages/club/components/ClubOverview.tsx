/**
 * ClubOverview Component
 * Displays club overview information and stats
 */

import React from 'react';
import { Calendar, Users, BookOpen } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import type { Club } from '@/global/models/club.models';

export interface ClubOverviewProps {
  club: Club;
  memberCount?: number;
  totalDiscussions?: number;
  totalMeetings?: number;
}

/**
 * ClubOverview component
 */
export const ClubOverview: React.FC<ClubOverviewProps> = ({
  club,
  memberCount = 0,
  totalDiscussions = 0,
  totalMeetings = 0,
}) => {
  // Format date to readable string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>About This Club</CardTitle>
        <CardDescription>
          Learn more about what this club offers
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Description */}
        {club.description && (
          <div>
            <h4 className="font-semibold mb-2">Description</h4>
            <p className="text-muted-foreground">{club.description}</p>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-start gap-3 p-4 border rounded-lg">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Users className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{memberCount}</p>
              <p className="text-sm text-muted-foreground">
                Active Members
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 border rounded-lg">
            <div className="p-2 bg-primary/10 rounded-lg">
              <BookOpen className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{totalDiscussions}</p>
              <p className="text-sm text-muted-foreground">
                Discussions
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 border rounded-lg">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Calendar className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{totalMeetings}</p>
              <p className="text-sm text-muted-foreground">
                Total Meetings
              </p>
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Created</span>
            <span className="font-medium">{formatDate(club.created_at)}</span>
          </div>
          {club.max_members && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Member Limit</span>
              <span className="font-medium">{club.max_members} members</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-muted-foreground">Status</span>
            <span className="font-medium">
              {club.is_active ? (
                <span className="text-green-600">Active</span>
              ) : (
                <span className="text-destructive">Inactive</span>
              )}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ClubOverview;
