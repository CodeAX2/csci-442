
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import javax.swing.JPanel;

public class MyPanel extends JPanel {

	BufferedImage grid;
	Graphics2D gc;

	public MyPanel() {
		setBackground(Color.BLACK);
	}

	public void clear() {
		grid = null;
		repaint();
	}
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		Graphics2D g2 = (Graphics2D)g;
		if (grid == null) {
			int w = this.getWidth();
			int h = this.getHeight();
			grid = (BufferedImage)(this.createImage(w, h));
			gc = grid.createGraphics();
			gc.setBackground(Color.BLACK);
			gc.clearRect(0, 0, w, h);
		}
		g2.drawImage(grid, null, 0, 0);
	}

	public void drawHistogram(Color color, int[] histogram) {
		gc.clearRect(0, 0, getWidth(), getHeight());
		gc.setColor(color);

		float maxValue = 0;

		for (int i = 0; i < histogram.length; i++) {
			if (histogram[i] > maxValue)
				maxValue = histogram[i];
		}

		for (int i = 0; i < histogram.length; i++) {
			gc.drawLine(
				i,
				getHeight(),
				i,
				getHeight() - (int)(histogram[i] / maxValue * getHeight() / 2f)
			);
		}
	}
}
