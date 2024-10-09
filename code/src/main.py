import os
import geopandas as gpd
import matplotlib.pyplot as plt

def plot_visited_countries(visited_countries, destination: str):
    """
    plots a map of European countries, highlighting the visited countries.
    :param visited_countries (set): a set of ISO Alpha-3 country codes for visited countries.
    :param destination: directory where image will be saved. defaults to the /Downloads folder.
    """
    # load geopolitical data of the countries in the world
    world = gpd.read_file('../resources/ne_10m_admin_0_countries.shp')
    # filter the data to include only countries in Europe and create a copy
    europe = world[world['CONTINENT'] == 'Europe'].copy()
    # add a 'visited' column to indicate if the country has been visited or not
    europe.loc[:, 'visited'] = europe['ISO_A3'].apply(lambda x: 'Visited' if x in visited_countries else 'Not Visited')
    # create the map
    fig, ax = plt.subplots(figsize=(16, 9))  # adjust figure size as needed
    ax.set_aspect('equal')  # set equal aspect ratio
    # color the visited and non-visited countries with different colors
    europe[europe['visited'] == 'Visited'].plot(ax=ax, color='blue', edgecolor='black', legend=True, label='Visited')
    europe[europe['visited'] == 'Not Visited'].plot(ax=ax, color='lightgray', edgecolor='black', legend=True, label='Not Visited')
    # set the axis limits based on the visited countries
    if not europe[europe['visited'] == 'Visited'].empty:
        bounds = europe[europe['visited'] == 'Visited'].total_bounds  # Get the bounds
        ax.set_xlim(bounds[0], bounds[2])  # set x-axis limits (xmin, xmax)
        ax.set_ylim(bounds[1], bounds[3])  # set y-axis limits (ymin, ymax)
    # map settings
    plt.axis('off')
    # show the map
    plt.show()
    # set default destination to /Downloads folder if not provided
    if destination is None:
        home = os.path.expanduser("~")  # get the user's home directory
        destination = os.path.join(home, "Downloads")  # append /Downloads
    # ensure destination directory exists
    if not os.path.exists(destination):
        os.makedirs(destination)
    # save the map image to the destination folder
    output_path = os.path.join(destination, 'european_countries_visited.png')
    fig.savefig(output_path, bbox_inches='tight', dpi=2400)  # save the figure

# example usage
if __name__ == "__main__":
    visited_countries = {"ITA", "ESP", "PRT", "AUT", "HUN", "GBR", "CZE", "GRC"}
    destination = None  # optional: specify destination path or leave None
    plot_visited_countries(visited_countries, destination)