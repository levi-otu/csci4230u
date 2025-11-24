/**
 * NextMeeting Component
 * Displays the next scheduled club meeting with details
 */

import React from 'react';
import { Calendar, Clock, MapPin, Video, BookOpen } from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/global/components/ui/card';
import { Badge } from '@/global/components/ui/badge';

export interface NextMeetingData {
  id: string;
  title: string;
  date: string;
  time: string;
  duration?: number; // in minutes
  location?: string;
  isVirtual: boolean;
  meetingLink?: string;
  chapters?: string[]; // e.g., ["Chapter 5", "Chapter 6"]
  agenda?: string;
  description?: string;
}

export interface NextMeetingProps {
  meeting: NextMeetingData | null;
}

/**
 * NextMeeting component
 */
export const NextMeeting: React.FC<NextMeetingProps> = ({ meeting }) => {
  // Format date to readable string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (!meeting) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Next Meeting</CardTitle>
          <CardDescription>
            No upcoming meetings scheduled
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="p-4 bg-muted rounded-full mb-4">
              <Calendar className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm text-muted-foreground">
              Check back later for upcoming meeting details
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Next Meeting</CardTitle>
        <CardDescription>
          Join us for the next book club discussion
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Meeting Title */}
        <div>
          <h3 className="text-lg font-semibold mb-2">{meeting.title}</h3>
          {meeting.description && (
            <p className="text-sm text-muted-foreground">
              {meeting.description}
            </p>
          )}
        </div>

        {/* Date and Time */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Calendar className="h-4 w-4 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium">Date</p>
              <p className="text-sm text-muted-foreground">
                {formatDate(meeting.date)}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Clock className="h-4 w-4 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium">Time</p>
              <p className="text-sm text-muted-foreground">
                {meeting.time}
                {meeting.duration && ` (${meeting.duration} min)`}
              </p>
            </div>
          </div>
        </div>

        {/* Location */}
        <div className="flex items-start gap-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            {meeting.isVirtual ? (
              <Video className="h-4 w-4 text-primary" />
            ) : (
              <MapPin className="h-4 w-4 text-primary" />
            )}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">
              {meeting.isVirtual ? 'Virtual Meeting' : 'Location'}
            </p>
            {meeting.isVirtual && meeting.meetingLink ? (
              <a
                href={meeting.meetingLink}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary hover:underline"
              >
                Join Meeting Link
              </a>
            ) : (
              <p className="text-sm text-muted-foreground">
                {meeting.location || 'Location TBD'}
              </p>
            )}
          </div>
        </div>

        {/* Chapters to be Covered */}
        {meeting.chapters && meeting.chapters.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-muted-foreground" />
              <p className="text-sm font-medium">Chapters to be Covered</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {meeting.chapters.map((chapter, index) => (
                <Badge key={index} variant="secondary">
                  {chapter}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Agenda */}
        {meeting.agenda && (
          <div className="space-y-2">
            <p className="text-sm font-medium">Agenda</p>
            <div className="p-3 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground whitespace-pre-line">
                {meeting.agenda}
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default NextMeeting;
