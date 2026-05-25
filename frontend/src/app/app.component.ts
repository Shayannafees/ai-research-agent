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
}
