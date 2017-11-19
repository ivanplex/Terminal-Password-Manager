#include <menu.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))
#define CTRLD 	4

char *choices[] = {
"Choice 1",
"Choice 2",
"Choice 3",
"Choice 4",
"Choice 5",
"Choice 6",
"Choice 7",
"Choice 8",
"Choice 9",
"Choice 10",
"Choice 11",
"Choice 12",
"Choice 13",
"Choice 14",
"Choice 15",
"Choice 16",
"Choice 17",
"Choice 18",
"Choice 19",
"Choice 20",
"Choice 21",
"Choice 22",
"Choice 23",
"Choice 24",
"Exit",
(char *)NULL,
};

void print_in_middle(WINDOW *win, int starty, int startx, int width, char *string, chtype color);

int main()
{	ITEM **identity;
	int c;				
	MENU *identity_menu;
    WINDOW *identity_menu_window;
    WINDOW *content_win;
    int n_choices, i;
	
	/* Initialize curses */
	initscr();
	start_color();
        cbreak();
        noecho();
	keypad(stdscr, TRUE);
	init_pair(1, COLOR_RED, COLOR_BLACK);

	/* Create items */
        n_choices = ARRAY_SIZE(choices);
        identity = (ITEM **)calloc(n_choices, sizeof(ITEM *));
        for(i = 0; i < n_choices; ++i)
                identity[i] = new_item(choices[i], NULL);

	/* Crate menu */
	identity_menu = new_menu((ITEM **)identity);

	/* Create the window to be associated with the menu */
        identity_menu_window = newwin(LINES -1, 30, 0, 0);
        keypad(identity_menu_window, TRUE);
     
	/* Set main window and sub window */
        set_menu_win(identity_menu, identity_menu_window);
        set_menu_sub(identity_menu, derwin(identity_menu_window, 40, 29, 3, 1));

	/* Set menu mark to the string " * " */
        set_menu_mark(identity_menu, "> ");

	/* Print a border around the main window and print a title */
        box(identity_menu_window, 0, 0);

    //Second window
    content_win = newwin(LINES -1, COLS-31, 0, 31);
    box(content_win, 0, 0);


	print_in_middle(identity_menu_window, 1, 0, 30, "Identity", COLOR_PAIR(1));
	mvwaddch(identity_menu_window, 2, 0, ACS_LTEE);
	mvwhline(identity_menu_window, 2, 1, ACS_HLINE, 30);
	mvwaddch(identity_menu_window, 2, 29, ACS_RTEE);
	mvprintw(LINES-1, 0, "F1 to exit");
	refresh();
        
	/* Post the menu */
	post_menu(identity_menu);
	wrefresh(identity_menu_window);
	wrefresh(content_win);

	while((c = wgetch(identity_menu_window)) != KEY_F(1))
	{       switch(c)
	        {	case KEY_DOWN:
				menu_driver(identity_menu, REQ_DOWN_ITEM);
				break;
			case KEY_UP:
				menu_driver(identity_menu, REQ_UP_ITEM);
				break;
		}
                wrefresh(identity_menu_window);
	}	

	/* Unpost and free all the memory taken up */
        unpost_menu(identity_menu);
        free_menu(identity_menu);
        for(i = 0; i < n_choices; ++i)
                free_item(identity[i]);
	endwin();
}

void print_in_middle(WINDOW *win, int starty, int startx, int width, char *string, chtype color)
{	int length, x, y;
	float temp;

	if(win == NULL)
		win = stdscr;
	getyx(win, y, x);
	if(startx != 0)
		x = startx;
	if(starty != 0)
		y = starty;
	if(width == 0)
		width = 60;

	length = strlen(string);
	temp = (width - length)/ 2;
	x = startx + (int)temp;
	wattron(win, color);
	mvwprintw(win, y, x, "%s", string);
	wattroff(win, color);
	refresh();
}