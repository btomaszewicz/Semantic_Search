def truncate_plot(plot_text):
        words = plot_text.split()
        if len(words) <= 10:
            return plot_text
        return ' '.join(words[:10]) + '...'
