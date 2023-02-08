/*
 *Hunter Lloyd
 * Copyrite.......I wrote, ask permission if you want to use it
 *outside of class.
 */

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.MemoryImageSource;
import java.awt.image.PixelGrabber;
import java.io.File;
import java.util.prefs.Preferences;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JScrollPane;

class IMP implements MouseListener {
	JFrame frame;
	JPanel mp;
	JButton start;
	JScrollPane scroll;
	JMenuItem openItem, exitItem, resetItem;
	Toolkit toolkit;
	File pic;
	ImageIcon img;
	int colorX, colorY;
	int[] pixels;
	int[] results;
	// Instance Fields you will be using below

	// This will be your height and width of your 2d array
	int height = 0, width = 0;
	int firstHeight = 0, firstWidth = 0;

	// your 2D array of pixels
	int picture[][];

	MyPanel redPanel, greenPanel, bluePanel;

	/**
	 * In the Constructor I set up the GUI, the frame the menus. The
	 * open pulldown menu is how you will open an image to manipulate.
	 */
	IMP() {
		toolkit = Toolkit.getDefaultToolkit();
		frame = new JFrame("Image Processing Software by Hunter");
		JMenuBar bar = new JMenuBar();
		JMenu file = new JMenu("File");
		JMenu functions = getFunctions();
		frame.addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent ev) {
				quit();
			}
		});
		openItem = new JMenuItem("Open");
		openItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				handleOpen();
			}
		});
		resetItem = new JMenuItem("Reset");
		resetItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				reset();
			}
		});
		exitItem = new JMenuItem("Exit");
		exitItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				quit();
			}
		});
		file.add(openItem);
		file.add(resetItem);
		file.add(exitItem);
		bar.add(file);
		bar.add(functions);
		frame.setSize(600, 600);
		mp = new JPanel();
		mp.setBackground(new Color(0, 0, 0));
		scroll = new JScrollPane(mp);
		frame.getContentPane().add(scroll, BorderLayout.CENTER);
		JPanel butPanel = new JPanel();
		butPanel.setBackground(Color.black);
		start = new JButton("start");
		start.setEnabled(false);
		start.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				drawHistograms();
			}
		});
		butPanel.add(start);
		frame.getContentPane().add(butPanel, BorderLayout.SOUTH);
		frame.setJMenuBar(bar);
		frame.setVisible(true);
	}

	/**
	 * This method creates the pulldown menu and sets up listeners to
	 * selection of the menu choices. If the listeners are activated
	 * they call the methods for handling the choice, fun1, fun2,
	 * fun3, fun4, etc. etc.
	 */

	private JMenu getFunctions() {
		JMenu fun = new JMenu("Functions");

		JMenuItem firstItem =
			new JMenuItem("MyExample - fun1 method");
		firstItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				fun1();
			}
		});
		fun.add(firstItem);

		// Add 90-degree roatation button
		JMenuItem secondItem = new JMenuItem("Rotate 90");
		secondItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				rotate90();
			}
		});
		fun.add(secondItem);

		// Add grayscale button
		JMenuItem thirdItem = new JMenuItem("Make Grayscale");
		thirdItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				makeGrayscale();
			}
		});
		fun.add(thirdItem);

		// Add grayscale and blur button
		JMenuItem fourthItem = new JMenuItem("Grayscale Blur");
		fourthItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				grayscaleBlur();
			}
		});
		fun.add(fourthItem);

		// Add edge mask button
		JMenuItem fifthItem = new JMenuItem("Edge Mask");
		fifthItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				edgeDetection();
			}
		});
		fun.add(fifthItem);

		// Add histrogram window button
		JMenuItem sixthItem = new JMenuItem("Open Histogram Window");
		sixthItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				openHistograms();
			}
		});
		fun.add(sixthItem);

		// Add histogram equalization button
		JMenuItem seventhItem = new JMenuItem("Equalize Histogram");
		seventhItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				histogramEQ();
			}
		});
		fun.add(seventhItem);

		return fun;
	}

	/**
	 * This method handles opening an image file, breaking down the
	 * picture to a one-dimensional array and then drawing the image
	 * on the frame. You don't need to worry about this method.
	 */
	private void handleOpen() {
		img = new ImageIcon();
		JFileChooser chooser = new JFileChooser();
		Preferences pref = Preferences.userNodeForPackage(IMP.class);
		String path = pref.get("DEFAULT_PATH", "");

		chooser.setCurrentDirectory(new File(path));
		int option = chooser.showOpenDialog(frame);

		if (option == JFileChooser.APPROVE_OPTION) {
			pic = chooser.getSelectedFile();
			pref.put("DEFAULT_PATH", pic.getAbsolutePath());
			img = new ImageIcon(pic.getPath());
		}
		width = img.getIconWidth();
		height = img.getIconHeight();
		firstWidth = width;
		firstHeight = height;

		JLabel label = new JLabel(img);
		label.addMouseListener(this);
		pixels = new int[width * height];

		results = new int[width * height];

		Image image = img.getImage();

		PixelGrabber pg = new PixelGrabber(
			image, 0, 0, width, height, pixels, 0, width
		);
		try {
			pg.grabPixels();
		} catch (InterruptedException e) {
			System.err.println("Interrupted waiting for pixels");
			return;
		}
		for (int i = 0; i < width * height; i++)
			results[i] = pixels[i];
		turnTwoDimensional();
		mp.removeAll();
		mp.add(label);

		mp.revalidate();
	}

	/**
	 * The libraries in Java give a one dimensional array of RGB
	 * values for an image, I thought a 2-Dimensional array would be
	 * more usefull to you So this method changes the one dimensional
	 * array to a two-dimensional.
	 */
	private void turnTwoDimensional() {
		picture = new int[height][width];
		for (int i = 0; i < height; i++)
			for (int j = 0; j < width; j++)
				picture[i][j] = pixels[i * width + j];
	}

	/**
	 * This method takes the picture back to the original picture
	 */
	private void reset() {
		height = firstHeight;
		width = firstWidth;
		for (int i = 0; i < width * height; i++)
			pixels[i] = results[i];
		Image img2 = toolkit.createImage(
			new MemoryImageSource(width, height, pixels, 0, width)
		);

		JLabel label2 = new JLabel(new ImageIcon(img2));
		mp.removeAll();
		mp.add(label2);

		mp.revalidate();
		mp.repaint();
		turnTwoDimensional();
	}

	/**
	 * This method is called to redraw the screen with the new image.
	 */
	private void resetPicture() {
		for (int i = 0; i < height; i++)
			for (int j = 0; j < width; j++)
				pixels[i * width + j] = picture[i][j];
		Image img2 = toolkit.createImage(
			new MemoryImageSource(width, height, pixels, 0, width)
		);

		JLabel label2 = new JLabel(new ImageIcon(img2));
		mp.removeAll();
		mp.add(label2);

		mp.revalidate();
		mp.repaint();
	}

	/**
	 * This method takes a single integer value and breaks it down
	 * doing bit manipulation to 4 individual int values for A, R, G,
	 * and B values
	 */
	private int[] getPixelArray(int pixel) {
		int temp[] = new int[4];
		temp[0] = (pixel >> 24) & 0xff;
		temp[1] = (pixel >> 16) & 0xff;
		temp[2] = (pixel >> 8) & 0xff;
		temp[3] = (pixel)&0xff;
		return temp;
	}

	/**
	 * This method takes an array of size 4 and combines the first 8
	 * bits of each to create one integer.
	 */
	private int getPixels(int rgb[]) {
		int alpha = 0;
		int rgba =
			(rgb[0] << 24) | (rgb[1] << 16) | (rgb[2] << 8) | rgb[3];
		return rgba;
	}

	public void getValue() {
		int pix = picture[colorY][colorX];
		int temp[] = getPixelArray(pix);
		System.out.println(
			"Color value " + temp[0] + " " + temp[1] + " " + temp[2] +
			" " + temp[3]
		);
	}

	/**************************************************************************************************
	 * This is where you will put your methods. Every method below is
	 *called when the corresponding pulldown menu is used. As long as
	 *you have a picture open first the when your fun1, fun2,
	 *fun....etc method is called you will have a 2D array called
	 *picture that is holding each pixel from your picture.
	 *************************************************************************************************/
	/**
	 * Example function that just removes all red values from the
	 * picture. Each pixel value in picture[i][j] holds an integer
	 * value. You need to send that pixel to getPixelArray the method
	 * which will return a 4 element array that holds A,R,G,B values.
	 * Ignore [0], that's the Alpha channel which is transparency, we
	 * won't be using that, but you can on your own. getPixelArray
	 * will breaks down your single int to 4 ints so you can
	 * manipulate the values for each level of R, G, B.
	 * After you make changes and do your calculations to your pixel
	 * values the getPixels method will put the 4 values in your ARGB
	 * array back into a single integer value so you can give it back
	 * to the program and display the new picture.
	 */
	private void fun1() {

		for (int i = 0; i < height; i++)
			for (int j = 0; j < width; j++) {
				int rgbArray[] = new int[4];

				// get three ints for R, G and B
				rgbArray = getPixelArray(picture[i][j]);

				rgbArray[1] = 0;
				// take three ints for R, G, B and put them back into
				// a single int
				picture[i][j] = getPixels(rgbArray);
			}
		resetPicture();
	}

	/**
	 * Rotates the image by 90 degrees and redraws it
	 */
	private void rotate90() {

		// Flip width/height
		int oldWidth = width, oldHeight = height;
		width = oldHeight;
		height = oldWidth;

		int[][] newPicture = new int[height][width];

		// Loop over each pixel
		for (int row = 0; row < oldHeight; row++) {
			for (int col = 0; col < oldWidth; col++) {
				// Map the old row/col to new row/col
				int mappedRow = height - col - 1;
				int mappedCol = row;
				newPicture[mappedRow][mappedCol] = picture[row][col];
			}
		}

		// Update the picture
		picture = newPicture;
		resetPicture();
	}

	/**
	 * Turns the image to grayscale using the luminosity algorithm
	 */
	private void makeGrayscale() {
		// Loop over each pixel
		for (int row = 0; row < height; row++) {
			for (int col = 0; col < width; col++) {
				// Get argb array
				int[] argb = getPixelArray(picture[row][col]);
				// Calculate the value
				int val = (int)(0.21 * argb[1] + 0.72 * argb[2] + 0.07 * argb[3]);
				// Update the picture
				argb[1] = val;
				argb[2] = val;
				argb[3] = val;
				picture[row][col] = getPixels(argb);
			}
		}
		resetPicture();
	}

	/**
	 * Turns the image to grayscale and performs a basic blur
	 */
	private void grayscaleBlur() {
		// Make the image grayscale
		makeGrayscale();

		// Save pixels to a new array
		int[][] newPicture = new int[height][width];
		// Loop over each pixel
		for (int row = 0; row < height; row++) {
			for (int col = 0; col < width; col++) {

				// Generate a total based on all 9 pixels
				float total = 0;
				float numSummed = 0;
				for (int offsetX = -1; offsetX <= 1; offsetX++) {
					for (int offsetY = -1; offsetY <= 1; offsetY++) {
						// Check the pixel is within bounds
						if (row + offsetY >= 0 &&
							row + offsetY < height &&
							col + offsetX >= 0 &&
							col + offsetX < width) {
							total += getPixelArray(
								picture[row + offsetY][col + offsetX]
							)[1];
							numSummed++;
						}
					}
				}
				// Calculate average
				int average = (int)(total / numSummed);
				newPicture[row][col] = getPixels(new int[] {
					255, average, average, average});
			}
		}
		// Update picture
		picture = newPicture;
		resetPicture();
	}

	/**
	 * Turns the image grayscale and performs edge detection using a
	 * 5x5 mask
	 */
	private void edgeDetection() {
		// Make the image grayscale
		makeGrayscale();

		// Use the 5x5 maks
		int[][] mask = {
			{-1, -1, -1, -1, -1},
			{-1, 0, 0, 0, -1},
			{-1, 0, 16, 0, -1},
			{-1, 0, 0, 0, -1},
			{-1, -1, -1, -1, -1}};

		// Create a new picture array
		int[][] newPicture = new int[height][width];

		// Loop over each pixel
		for (int row = 0; row < height; row++) {
			for (int col = 0; col < width; col++) {

				// Calculate the new value for the pixel
				int newValue = 0;

				// Loop over each spot of the mask
				for (int maskY = 0; maskY < mask.length; maskY++) {
					for (int maskX = 0; maskX < mask[maskY].length; maskX++) {
						// Generate the offsets
						int offsetY = -(mask.length / 2) + maskY;
						int offsetX =
							-(mask[maskY].length / 2) + maskX;

						// Check the offset is in the bounds
						if (row + offsetY >= 0 &&
							row + offsetY < height &&
							col + offsetX >= 0 &&
							col + offsetX < width) {
							// Calculate value based on the mask 
							newValue +=
								mask[maskY][maskX] *
								getPixelArray(picture[row + offsetY][col + offsetX])[1];
						}
					}
				}

				// Anthing below 50 goes to black, above 50 goes to white
				if (newValue < 50)
					newValue = 0;
				if (newValue >= 50)
					newValue = 255;

				newPicture[row][col] = getPixels(new int[] {
					255, newValue, newValue, newValue});
			}
		}

		// Update the picture
		picture = newPicture;
		resetPicture();
	}

	/**
	 * Opens windows to view the histogram of the image
	 */
	private void openHistograms() {
		// Create the histogram frame
		JFrame histogramFrame = new JFrame("Histograms");
		histogramFrame.setSize(915, 600);
		histogramFrame.setLocation(600, 0);
		histogramFrame.addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent ev) {
				start.setEnabled(false);
			}
		});

		// Create a container to contain all 3 histogram panels
		JPanel container = new JPanel();
		container.setLayout(new BoxLayout(container, BoxLayout.X_AXIS)
		);

		// Create the histogram panels
		redPanel = new MyPanel();
		container.add(redPanel);

		greenPanel = new MyPanel();
		container.add(greenPanel);

		bluePanel = new MyPanel();
		container.add(bluePanel);

		histogramFrame.getContentPane().add(container);
		histogramFrame.setVisible(true);

		// Enable the start button
		start.setEnabled(true);
	}

	/**
	 * Draws the histograms to the histogram panels
	 */
	private void drawHistograms() {
		// Create arrays for the histograms
		int[] red = new int[256];
		int[] green = new int[256];
		int[] blue = new int[256];
		// Increment array values
		for (int i = 0; i < pixels.length; i++) {
			int[] curPixelData = getPixelArray(pixels[i]);
			red[curPixelData[1]]++;
			green[curPixelData[2]]++;
			blue[curPixelData[3]]++;
		}
		// Draw the histograms
		redPanel.drawHistogram(Color.RED, red);
		greenPanel.drawHistogram(Color.GREEN, green);
		bluePanel.drawHistogram(Color.BLUE, blue);

		redPanel.repaint();
		greenPanel.repaint();
		bluePanel.repaint();
	}

	/**
	 * Equalizes the image based on its histogram
	 */
	private void histogramEQ() {
		// Get the R,G,B histograms
		int[] red = new int[256];
		int[] green = new int[256];
		int[] blue = new int[256];
		for (int i = 0; i < pixels.length; i++) {
			int[] curPixelData = getPixelArray(pixels[i]);
			red[curPixelData[1]]++;
			green[curPixelData[2]]++;
			blue[curPixelData[3]]++;
		}

		// Generate the new rgb value mappings
		int totalPixels = width * height;
		int[] newRed = generateCumulative(red, totalPixels);
		int[] newGreen = generateCumulative(green, totalPixels);
		int[] newBlue = generateCumulative(blue, totalPixels);

		// Update the pixels based on the mappings
		for (int row = 0; row < height; row++) {
			for (int col = 0; col < width; col++) {
				int pixel = picture[row][col];
				int[] pixelColors = getPixelArray(pixel);
				pixelColors[1] = newRed[pixelColors[1]];
				pixelColors[2] = newGreen[pixelColors[2]];
				pixelColors[3] = newBlue[pixelColors[3]];
				picture[row][col] = getPixels(pixelColors);
			}
		}
		resetPicture();
	}

	/**
	 * Generates an array mapping the original color value to 
	 * its new color value for histogram normalization
	 * @param colArr The original color histogram array
	 * @param totalPixels the total number of pixels in the image
	 * @return The cumulative color array
	 */
	private int[] generateCumulative(int[] colArr, int totalPixels) {
		int[] cumulativeValues = new int[colArr.length];
		float total = 0;
		for (int i = 0; i < colArr.length; i++) {
			total += colArr[i];
			cumulativeValues[i] =
				Math.round(total / totalPixels * (colArr.length - 1));
		}
		return cumulativeValues;
	}

	private void quit() {
		System.exit(0);
	}

	@Override
	public void mouseEntered(MouseEvent m) {}

	@Override
	public void mouseExited(MouseEvent m) {}

	@Override
	public void mouseClicked(MouseEvent m) {
		colorX = m.getX();
		colorY = m.getY();
		System.out.println(colorX + "  " + colorY);
		getValue();
		start.setEnabled(true);
	}

	@Override
	public void mousePressed(MouseEvent m) {}

	@Override
	public void mouseReleased(MouseEvent m) {}

	public static void main(String[] args) {
		IMP imp = new IMP();
	}
}
