import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Location } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, Message, Session } from './services/chat.service';
import { ChatWindowComponent } from './components/chat-window/chat-window.component';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatWindowComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  title = 'AI Chatbot';

  messages: Message[] = [];
  recentSessions: Session[] = [];
  currentSession: Session | null = null;
  userInput = '';
  isLoading = false;
  errorMessage = '';

  constructor(
    private chatService: ChatService,
    private cdr: ChangeDetectorRef,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.loadSessions(true);
  }

  loadSessions(autoSelectFirst: boolean = true): void {
    this.chatService.getSessions().subscribe({
      next: (sessions) => {
        this.recentSessions = sessions;
        // Check for sessionId in URL query params
        const queryParams = new URLSearchParams(window.location.search);
        const urlSessionId = queryParams.get('sessionId');
        if (urlSessionId) {
          const matching = sessions.find(s => s.session_id === urlSessionId);
          if (matching) {
            this.selectSession(matching);
          } else {
            // If not found, fallback to auto selection
            this.autoSelectSession(sessions, autoSelectFirst);
          }
        } else {
          this.autoSelectSession(sessions, autoSelectFirst);
        }
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to load sessions:', err);
      }
    });
  }

  private autoSelectSession(sessions: Session[], autoSelectFirst: boolean): void {
    if (autoSelectFirst) {
      if (sessions.length > 0) {
        const activeExists = this.currentSession && sessions.some(s => s.session_id === this.currentSession?.session_id);
        if (!activeExists) {
          this.selectSession(sessions[0]);
        }
      } else {
        this.createNewSession();
      }
    }
  }

  selectSession(session: Session): void {
    this.currentSession = session;
    this.errorMessage = '';
    this.isLoading = true;
    this.messages = [];
    // Update URL with sessionId
    this.location.replaceState(`?sessionId=${session.session_id}`);
    this.chatService.getSessionMessages(session.session_id).subscribe({
      next: (msgs) => {
        this.messages = msgs;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to load messages:', err);
        this.isLoading = false;
        this.errorMessage = 'Failed to load message history.';
        this.cdr.detectChanges();
      }
    });
  }

  createNewSession(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.chatService.createSession('New Conversation').subscribe({
      next: (session) => {
        this.currentSession = session;
        this.messages = [];
        this.isLoading = false;
        this.loadSessions(false);
        this.recentSessions = [session, ...this.recentSessions];
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to create session:', err);
        this.isLoading = false;
        this.errorMessage = 'Failed to create a new session.';
        this.cdr.detectChanges();
      }
    });
  }

  sendMessage(): void {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    if (!this.currentSession) {
      this.errorMessage = 'No active session selected. Creating a new session...';
      this.createNewSession();
      return;
    }

    this.userInput = '';
    this.errorMessage = '';
    this.isLoading = true;

    // Optimistically add user message
    this.messages = [...this.messages, { role: 'user', content: text }];

    this.chatService.sendMessage(this.currentSession.session_id, text).subscribe({
      next: (res) => {
        console.log('Received response:', res);
        this.messages = [
          ...this.messages,
          { role: 'assistant', content: res.reply },
        ];
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Chat error:', err);
        this.isLoading = false;
        this.errorMessage =
          err?.error?.detail ?? err?.error?.error ?? 'Failed to reach the server. Is the backend running?';
        this.cdr.detectChanges();
      },
    });
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  clearChat(): void {
    if (!this.currentSession) return;

    const idToDelete = this.currentSession.session_id;
    this.isLoading = true;
    this.errorMessage = '';

    this.chatService.deleteSession(idToDelete).subscribe({
      next: () => {
        this.currentSession = null;
        this.messages = [];
        this.loadSessions(true);
      },
      error: (err) => {
        console.error('Failed to delete session:', err);
        this.isLoading = false;
        this.errorMessage = 'Failed to delete session.';
        this.cdr.detectChanges();
      }
    });
  }
}
