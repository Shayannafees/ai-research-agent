import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResearchService } from './research.service';
import { FormsModule } from '@angular/forms';
// import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  constructor(private researchService: ResearchService){}
  title = 'frontend';

  question = '';
  answer = '';
  isLoading = false;

  ask() {
    this.isLoading = true;
    this.answer = '';
    this.researchService.askStream(this.question, (token)=> this.answer += token, ()=> this.isLoading = false)
  }

  get formattedAnswer(): string {
    return this.answer
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/^## (.+)$/gm, '<h2>$1</h2>')
      .replace(/^# (.+)$/gm, '<h1>$1</h1>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/^- (.+)$/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
      .replace(/\n/g, '<br>');
  }
}
